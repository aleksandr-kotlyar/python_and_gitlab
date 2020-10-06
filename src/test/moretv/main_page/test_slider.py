from selene import have, be


def test_arrows_are_visible(browser_module):
    """Main Page Slider should have 2 arrows. Arrows should be visible."""
    browser_module.open('https://more.tv')

    browser_module.all('.slick-slider [filter]').should(have.size(2))
    browser_module.all('.slick-slider [filter]').should(be.visible)
