from django.test import TestCase
from sample.models import Item

class VersionedModelTest(TestCase):
    def test_version_initial_value(self):
        """Test that the version is 1 upon creation."""
        item = Item.objects.create(name="Test Item")
        self.assertEqual(item.version, 1)

    def test_version_increments_on_save(self):
        """Test that the version increments on each save."""
        item = Item.objects.create(name="Test Item")
        self.assertEqual(item.version, 1)

        item.name = "Updated Item"
        item.save()
        self.assertEqual(item.version, 2)

        item.description = "Some description"
        item.save()
        self.assertEqual(item.version, 3)
