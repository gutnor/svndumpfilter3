__author__ = 'vderijcke'

import unittest
from svndumpfilter3 import *


class TestStandardPath(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(StandardPath("test/trunk").valid)
        self.assertTrue(StandardPath("test/trunk/file").valid)
        self.assertTrue(StandardPath("test/trunk/path/to/file.java").valid)

        self.assertTrue(StandardPath("test/branches/version1.0").valid)
        self.assertTrue(StandardPath("test/tags/version1.0").valid)

        self.assertTrue(StandardPath("test/branches/version1.0/file").valid)
        self.assertTrue(StandardPath("test/tags/version1.0/file").valid)

        self.assertTrue(StandardPath("test/branches/version1.0/path/to/file.java").valid)
        self.assertTrue(StandardPath("test/tags/version1.0/path/to/file.java").valid)

    def test_root(self):
        self.assertTrue(StandardPath("test/trunk").isRoot())
        self.assertFalse(StandardPath("test/trunk/file").isRoot())
        self.assertFalse(StandardPath("test/trunk/path/to/file.java").isRoot())

        self.assertTrue(StandardPath("test/branches/version1.0").isRoot())
        self.assertTrue(StandardPath("test/tags/version1.0").isRoot())

        self.assertFalse(StandardPath("test/branches/version1.0/file").isRoot())
        self.assertFalse(StandardPath("test/tags/version1.0/file").isRoot())

        self.assertFalse(StandardPath("test/branches/version1.0/path/to/file.java").isRoot())
        self.assertFalse(StandardPath("test/tags/version1.0/path/to/file.java").isRoot())

    def test_invalid(self):
        self.assertFalse(StandardPath("test").valid)
        self.assertFalse(StandardPath("trunk").valid)
        self.assertFalse(StandardPath("branches").valid)
        self.assertFalse(StandardPath("tags").valid)
        self.assertFalse(StandardPath("project/tags2").valid)
        self.assertFalse(StandardPath("project/mybranches").valid)
        self.assertFalse(StandardPath("project/trunkish").valid)

    def test_trunk(self):
        trunk = StandardPath("test/trunk/path/to/file.java")
        self.assertTrue(trunk.valid)

        self.assertTrue(trunk.trunk)
        self.assertFalse(trunk.branch)
        self.assertFalse(trunk.tag)

        self.assertEquals(trunk.project, "test")
        self.assertEquals(trunk.filepath, "/path/to/file.java")

    def test_branch(self):
        branch = StandardPath("test/branches/version1.0/path/to/file.java")
        self.assertTrue(branch.valid)

        self.assertFalse(branch.trunk)
        self.assertTrue(branch.branch)
        self.assertFalse(branch.tag)

        self.assertEquals(branch.branch, "version1.0")
        self.assertEquals(branch.project, "test")
        self.assertEquals(branch.filepath, "/path/to/file.java")

    def test_tag(self):
        tag = StandardPath("test/tags/version1.0/path/to/file.java")
        self.assertTrue(tag.valid)

        self.assertFalse(tag.trunk)
        self.assertFalse(tag.branch)
        self.assertTrue(tag.tag)

        self.assertEquals(tag.tag, "version1.0")
        self.assertEquals(tag.project, "test")
        self.assertEquals(tag.filepath, "/path/to/file.java")

    def assertSameVersion(self, a, b):
        self.assertTrue(StandardPath(a).equalsVersion(StandardPath(b)))

    def assertDifferentVersion(self, a, b):
        self.assertFalse(StandardPath(a).equalsVersion(StandardPath(b)))

    def test_equalsVersion(self):
        self.assertSameVersion("test/tags/version1.0/path/to/file.java",
                               "test/tags/version1.0")
        self.assertSameVersion("test/tags/version1.0/path/to/file.java",
                               "test/tags/version1.0/file")

        self.assertSameVersion("test/branches/version1.0/path/to/file.java",
                               "test/branches/version1.0")
        self.assertSameVersion("test/branches/version1.0/path/to/file.java",
                               "test/branches/version1.0/file")

        self.assertDifferentVersion("test/branches/version1.0/path/to/file.java",
                                    "test/tags/version1.0/path/to/file.java")
        self.assertDifferentVersion("test/branches/version1.0/path/to/file.java",
                                    "test/trunk/path/to/file.java")

if __name__ == '__main__':
    unittest.main()


