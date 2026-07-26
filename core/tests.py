from django.test import TestCase
from sample.models import Item
from django.utils import timezone

class SoftDeleteTest(TestCase):
    def test_delete(self):
        """Test that calling delete() sets is_deleted to True and sets deleted_at."""
        obj = Item.objects.create(name='test_delete')
        self.assertFalse(obj.is_deleted)
        self.assertIsNone(obj.deleted_at)

        before_delete = timezone.now()
        obj.delete()
        after_delete = timezone.now()

        self.assertTrue(obj.is_deleted)
        self.assertIsNotNone(obj.deleted_at)
        self.assertTrue(before_delete <= obj.deleted_at <= after_delete)

    def test_restore(self):
        """Test that calling restore() sets is_deleted to False."""
        obj = Item.objects.create(name='test_restore')
        obj.delete()
        self.assertTrue(obj.is_deleted)

        obj.restore()
        self.assertFalse(obj.is_deleted)
        # Note: Depending on the implementation of restore, it may or may not clear deleted_at.
        # As per the code provided in the original issue description, it only sets is_deleted = False.
        # But wait, the master branch of core/models.py DOES set deleted_at = None and calls save()
        # So I will assert that.
        self.assertIsNone(obj.deleted_at)

    def test_managers(self):
        """Test that the default manager filters out deleted items while all_objects doesn't."""
        item1 = Item.objects.create(name='item1')
        item2 = Item.objects.create(name='item2')
        item2.delete()

        # Test SoftDeleteManager (default objects manager)
        self.assertEqual(Item.objects.count(), 1)
        self.assertIn(item1, Item.objects.all())
        self.assertNotIn(item2, Item.objects.all())

        # Test all_objects manager
        self.assertEqual(Item.all_objects.count(), 2)
        self.assertIn(item1, Item.all_objects.all())
        self.assertIn(item2, Item.all_objects.all())

    def test_delete_multiple_times(self):
        """Test that calling delete() multiple times updates deleted_at but doesn't cause errors."""
        obj = Item.objects.create(name='test_delete_multi')
        obj.delete()
        first_deleted_at = obj.deleted_at

        obj.delete()
        second_deleted_at = obj.deleted_at

        self.assertTrue(obj.is_deleted)
        self.assertTrue(second_deleted_at >= first_deleted_at)
