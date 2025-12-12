"""CSV import service for processing product feeds."""
import logging
import csv
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.mysql import insert as mysql_insert

from app.core.config import settings
from app.models.product import Product, Category, Manufacturer, ProductCategory
from app.models.eav import Attribute, AttributeValue, AttributeType
from app.models.feed import InboundFeed, FeedStatus


logger = logging.getLogger(__name__)


class ImportService:
    """Service for importing product CSV feeds."""

    def __init__(self, db: AsyncSession, feed_id: int):
        """Initialize import service."""
        self.db = db
        self.feed_id = feed_id
        self.chunk_size = settings.CSV_CHUNK_SIZE
        self.logs = []

    async def import_feed(self) -> bool:
        """Import feed from file."""
        try:
            # Get feed record
            result = await self.db.execute(
                select(InboundFeed).where(InboundFeed.id == self.feed_id)
            )
            feed = result.scalar_one_or_none()

            if not feed:
                logger.error(f"Feed not found: {self.feed_id}")
                return False

            # Update status
            feed.status = FeedStatus.PROCESSING
            feed.started_at = datetime.utcnow()
            await self.db.commit()

            # Process CSV file
            await self._process_csv(feed)

            # Update final status
            if feed.error_count == 0:
                feed.status = FeedStatus.COMPLETED
            elif feed.success_count > 0:
                feed.status = FeedStatus.PARTIAL
            else:
                feed.status = FeedStatus.FAILED

            feed.completed_at = datetime.utcnow()
            feed.processing_logs = json.dumps(self.logs)
            await self.db.commit()

            return True

        except Exception as e:
            logger.error(f"Import failed: {e}", exc_info=True)
            # Update feed status
            result = await self.db.execute(
                select(InboundFeed).where(InboundFeed.id == self.feed_id)
            )
            feed = result.scalar_one_or_none()
            if feed:
                feed.status = FeedStatus.FAILED
                feed.error_message = str(e)
                feed.processing_logs = json.dumps(self.logs)
                await self.db.commit()
            return False

    async def _process_csv(self, feed: InboundFeed):
        """Process CSV file in chunks."""
        chunk = []
        row_count = 0

        with open(feed.file_path, 'r', encoding='utf-8') as csvfile:
            # Auto-detect delimiter
            sample = csvfile.read(1024)
            csvfile.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter

            reader = csv.DictReader(csvfile, delimiter=delimiter)

            # Normalize headers
            reader.fieldnames = [self._normalize_header(h) for h in reader.fieldnames]

            for row in reader:
                row_count += 1
                chunk.append(row)

                if len(chunk) >= self.chunk_size:
                    await self._process_chunk(chunk, feed)
                    chunk = []

            # Process remaining rows
            if chunk:
                await self._process_chunk(chunk, feed)

        feed.total_count = row_count
        self._add_log("info", f"Processed {row_count} rows")

    async def _process_chunk(self, chunk: List[Dict], feed: InboundFeed):
        """Process a chunk of rows."""
        success_count = 0
        error_count = 0

        for row in chunk:
            try:
                await self._process_row(row, feed.entity_code)
                success_count += 1
            except Exception as e:
                error_count += 1
                logger.error(f"Row processing error: {e}")
                self._add_log("error", f"Row error: {str(e)[:100]}")

        # Update feed counts
        feed.success_count += success_count
        feed.error_count += error_count
        feed.pending_count = feed.total_count - (feed.success_count + feed.error_count)

        await self.db.commit()

    async def _process_row(self, row: Dict[str, Any], entity_code: str):
        """Process a single CSV row."""
        # Extract core product fields
        sku = row.get("sku") or row.get("product_sku")
        if not sku:
            raise ValueError("SKU is required")

        product_data = {
            "sku": sku,
            "entity_code": entity_code,
            "name": row.get("name") or row.get("product_name", ""),
            "description": row.get("description", ""),
            "price": self._parse_decimal(row.get("price", 0)),
            "cost": self._parse_decimal(row.get("cost")),
            "retail_price": self._parse_decimal(row.get("retail_price")),
            "qty": int(row.get("qty", 0) or 0),
            "min_qty": int(row.get("min_qty", 0) or 0),
            "images": row.get("images", ""),
            "raw_data": json.dumps(row),
            "is_active": 1
        }

        # Handle manufacturer
        if row.get("manufacturer"):
            manufacturer = await self._get_or_create_manufacturer(row["manufacturer"])
            product_data["manufacturer_id"] = manufacturer.id

        # Upsert product
        product = await self._upsert_product(product_data)

        # Handle categories
        if row.get("categories"):
            await self._process_categories(product, row["categories"])

        # Handle EAV attributes
        await self._process_attributes(product, row)

    async def _upsert_product(self, product_data: Dict) -> Product:
        """Insert or update product."""
        # Try to find existing product
        result = await self.db.execute(
            select(Product).where(
                Product.sku == product_data["sku"],
                Product.entity_code == product_data["entity_code"]
            )
        )
        product = result.scalar_one_or_none()

        if product:
            # Update existing
            for key, value in product_data.items():
                setattr(product, key, value)
        else:
            # Create new
            product = Product(**product_data)
            self.db.add(product)

        await self.db.flush()
        return product

    async def _get_or_create_manufacturer(self, name: str) -> Manufacturer:
        """Get or create manufacturer."""
        result = await self.db.execute(
            select(Manufacturer).where(Manufacturer.name == name)
        )
        manufacturer = result.scalar_one_or_none()

        if not manufacturer:
            manufacturer = Manufacturer(name=name, is_system=1)
            self.db.add(manufacturer)
            await self.db.flush()

        return manufacturer

    async def _process_categories(self, product: Product, categories_str: str):
        """Process product categories."""
        category_names = [c.strip() for c in categories_str.split(",")]

        for idx, cat_name in enumerate(category_names):
            # Get or create category
            result = await self.db.execute(
                select(Category).where(Category.name == cat_name)
            )
            category = result.scalar_one_or_none()

            if not category:
                category = Category(
                    name=cat_name,
                    code=cat_name.lower().replace(" ", "_"),
                    level=0
                )
                self.db.add(category)
                await self.db.flush()

            # Link product to category
            result = await self.db.execute(
                select(ProductCategory).where(
                    ProductCategory.product_id == product.id,
                    ProductCategory.category_id == category.id
                )
            )
            pc = result.scalar_one_or_none()

            if not pc:
                pc = ProductCategory(
                    product_id=product.id,
                    category_id=category.id,
                    is_primary=1 if idx == 0 else 0
                )
                self.db.add(pc)

    async def _process_attributes(self, product: Product, row: Dict):
        """Process EAV attributes."""
        # Skip core fields
        core_fields = {"sku", "product_sku", "name", "product_name", "description",
                       "price", "cost", "retail_price", "qty", "min_qty",
                       "manufacturer", "categories", "images"}

        for field_name, value in row.items():
            if field_name in core_fields or not value:
                continue

            # Get or create attribute
            attribute = await self._get_or_create_attribute(field_name)

            # Set attribute value
            await self._set_attribute_value(product, attribute, value)

    async def _get_or_create_attribute(self, code: str) -> Attribute:
        """Get or create attribute."""
        result = await self.db.execute(
            select(Attribute).where(Attribute.code == code)
        )
        attribute = result.scalar_one_or_none()

        if not attribute:
            # Auto-detect type
            attribute = Attribute(
                code=code,
                label=code.replace("_", " ").title(),
                attribute_type=AttributeType.VARCHAR,
                input_type="text",
                is_system=1
            )
            self.db.add(attribute)
            await self.db.flush()

        return attribute

    async def _set_attribute_value(self, product: Product, attribute: Attribute, value: Any):
        """Set attribute value."""
        # Find existing value
        result = await self.db.execute(
            select(AttributeValue).where(
                AttributeValue.product_id == product.id,
                AttributeValue.attribute_id == attribute.id
            )
        )
        attr_value = result.scalar_one_or_none()

        if not attr_value:
            attr_value = AttributeValue(
                product_id=product.id,
                attribute_id=attribute.id
            )
            self.db.add(attr_value)

        # Set value based on type
        if attribute.attribute_type == AttributeType.VARCHAR:
            attr_value.value_varchar = str(value)[:500]
        elif attribute.attribute_type == AttributeType.TEXT:
            attr_value.value_text = str(value)
        elif attribute.attribute_type == AttributeType.INT:
            try:
                attr_value.value_int = int(value)
            except:
                pass
        elif attribute.attribute_type == AttributeType.DECIMAL:
            attr_value.value_decimal = str(self._parse_decimal(value))

    def _normalize_header(self, header: str) -> str:
        """Normalize CSV header."""
        return header.strip().lower().replace(" ", "_").replace("-", "_")

    def _parse_decimal(self, value: Any) -> Optional[Decimal]:
        """Parse decimal value."""
        if value is None or value == "":
            return None
        try:
            return Decimal(str(value))
        except:
            return None

    def _add_log(self, level: str, message: str):
        """Add log entry."""
        self.logs.append({
            "level": level,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        })
