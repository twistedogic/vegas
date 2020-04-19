import unittest
from collections import namedtuple

from src.vegas.data import Crawler


class TestCrawler(unittest.TestCase):
    def test_get_links(self) -> None:
        testcase = namedtuple("_get_links_case", ["content", "root", "want"])
        cases = dict(
            base=testcase(
                content="""
            <a href="/test.php">
            <a href="/test.php">
            <a href="/test.php">
            <a href="/test.js">
            <a href="/test.csv">
            <a href="http://other.domain/test.html">
            """,
                root="http://localhost",
                want=[
                    "http://localhost/test.php",
                    "http://localhost/test.csv",
                    "http://localhost/test.js",
                ],
            )
        )
        for name, tc in cases.items():
            crawler = Crawler(url=tc.root)
            got = crawler._get_links(tc.content)
            assert got == tc.want
