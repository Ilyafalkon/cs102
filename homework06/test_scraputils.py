import pytest
from bs4 import BeautifulSoup

from scraputils import extract_news, get_news


class TestExtractNews:
    @pytest.fixture()
    def html_with_news(self):
        return """
                <html lang="en" op="news">
                <head>
                    <title>Hacker News</title>
                </head>
                <body>
                    <center>
                        <table id="hnmain" border="0" cellpadding="0" cellspacing="0" width="85%" bgcolor="#f6f6ef">
                            <tr>
                                <td bgcolor="#ff6600">
                                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding:2px">
                                        <tr>
                                            here is title we don't need
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr id="pagespace" title="" style="height:10px"></tr>
                            <tr>
                                <td>
                                    <table border="0" cellpadding="0" cellspacing="0" class="itemlist">
                                        <tr class='athing' id='26803201'>
                                            <td align="right" valign="top" class="title">
                                                <span class="rank">1.</span>
                                            </td>
                                            <td valign="top" class="votelinks">
                                                <center>
                                                    <a id='up_26803201' href='vote?id=26803201&amp;how=up&amp;goto=news'>
                                                        <div class='votearrow' title='upvote'></div>
                                                    </a>
                                                </center>
                                            </td>
                                            <td class="title">
                                                <a href="https://y-n10.com/" class="storylink">Yamauchi No.10 Family Office</a>
                                                <span class="sitebit comhead">
                                                     (
                                                    <a href="from?site=y-n10.com">
                                                        
                                                        {link}
                                                        
                                                    </a>
                                                    )
                                                </span>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="2"></td>
                                            <td class="subtext">
                                            
                                                {score_n_author}
                                                
                                                <span class="age">
                                                    <a href="item?id=26803201">4 hours ago</a>
                                                </span>
                                                <span id="unv_26803201"></span>
                                                 | 
                                                <a href="hide?id=26803201&amp;goto=news">hide</a>
                                                 | 
                                                <a href="item?id=26803201">88&nbsp;comments</a>
                                            </td>
                                        </tr>
                                        <tr class="spacer" style="height:5px"></tr>
                                        <tr class="morespace" style="height:10px"></tr>
                                        <tr>
                                            <td colspan="2"></td>
                                            <td class="title">
                                                <a href="news?p=2" class="morelink" rel="next">More</a>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>  
                            <tr>
                                <td>
                                    <table width="100%" cellspacing="0" cellpadding="1">
                                        <tr>
                                            <td bgcolor="#ff6600"></td>
                                        </tr>
                                    </table>
                                    <br>
                                    <center>
                                        and here are an elements we don't need
                                    </center>
                                </td>
                            </tr>
                        </table>
                    </center>
                </body>
                </html>
                """

    @pytest.fixture()
    def html_without_news(self):
        return """
                <html lang="en" op="news">
                    <head>
                        <title>Hacker News</title>
                    </head>
                    <body>
                        <center>
                            <table id="hnmain" border="0" cellpadding="0" cellspacing="0" width="85%" bgcolor="#f6f6ef">
                                <tr>
                                    <td bgcolor="#ff6600">
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding:2px">
                                            <tr>
                                                title we don't need
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr id="pagespace" title="" style="height:10px"></tr>
                                <tr>
                                    <td>
                                        <table border="0" cellpadding="0" cellspacing="0" class="itemlist">
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <table width="100%" cellspacing="0" cellpadding="1">
                                            <tr>
                                                <td bgcolor="#ff6600"></td>
                                            </tr>
                                        </table>
                                        <br>
                                        <center>
                                            nothing we need
                                        </center>
                                    </td>
                                </tr>
                            </table>
                        </center>
                    </body>
                </html>
                """

    def test_with_full_amount_of_data(self, html_with_news):
        # fmt: off
        html = html_with_news.format(link='<span class="sitestr">y-n10.com</span>', score_n_author='<span class="score" id="score_26803201">297 points</span> by <a href="user?id=cmod" class="hnuser">cmod</a>')
        # fmt: on
        page = BeautifulSoup(html, "html.parser")
        news_list = extract_news(page)
        expected_news_list = [
            {
                "title": "Yamauchi No.10 Family Office",
                "short_url": "y-n10.com",
                "long_url": "https://y-n10.com/",
                "score": 297,
                "author": "cmod",
            }
        ]

        assert expected_news_list.sort() == news_list.sort()

    def test_without_short_link(self, html_with_news):
        # fmt: off
        html = html_with_news.format(link='', score_n_author='<span class="score" id="score_26803201">297 points</span> by <a href="user?id=cmod" class="hnuser">cmod</a>')
        # fmt: on
        page = BeautifulSoup(html, "html.parser")
        news_list = extract_news(page)
        expected_news_list = [
            {
                "title": "Yamauchi No.10 Family Office",
                "short_url": "news.ycombinator.com",
                "long_url": "https://news.ycombinator.com/https://y-n10.com/",
                "score": 297,
                "author": "cmod",
            }
        ]

        assert expected_news_list.sort() == news_list.sort()

    def test_without_author(self, html_with_news):
        # fmt: off
        html = html_with_news.format(link='<span class="sitestr">y-n10.com</span>', score_n_author='<span class="score" id="score_26803201">297 points</span>')
        # fmt: on
        page = BeautifulSoup(html, "html.parser")
        news_list = extract_news(page)
        expected_news_list = [
            {
                "title": "Yamauchi No.10 Family Office",
                "short_url": "y-n10.com",
                "long_url": "https://y-n10.com/",
                "score": 297,
                "author": "-",
            }
        ]

        assert expected_news_list.sort() == news_list.sort()

    def test_without_score(self, html_with_news):
        # fmt: off
        html = html_with_news.format(link='<span class="sitestr">y-n10.com</span>', score_n_author='<a href="user?id=cmod" class="hnuser">cmod</a>')
        # fmt: on
        page = BeautifulSoup(html, "html.parser")
        news_list = extract_news(page)
        expected_news_list = [
            {
                "title": "Yamauchi No.10 Family Office",
                "short_url": "y-n10.com",
                "long_url": "https://y-n10.com/",
                "score": 0,
                "author": "cmod",
            }
        ]

        assert expected_news_list.sort() == news_list.sort()
