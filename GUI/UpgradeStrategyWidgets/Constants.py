


def returnUpgradeStrategies() -> dict[str, type]:
    from GUI.UpgradeStrategyWidgets.IncrementalUpgradeWidget import IncrementalUpgrade
    from GUI.UpgradeStrategyWidgets.BasicUpgradeWidget import BasicUpgradeWidget
    from GUI.UpgradeStrategyWidgets.InfluencedUpgradeWidget import InfluencedUpgradeWidget
    from GUI.UpgradeStrategyWidgets.ConditionalUpgrade import ConditionalUpgradeWidget
    from GUI.UpgradeStrategyWidgets.BundledStrategy import BundledStrategy
    from GUI.UpgradeStrategyWidgets.RandomUpgradeWidget import RandomUpgradeWidget
    strategies = {
        # "Apply Effect Upgrade": None,
        "Basic Upgrade": BasicUpgradeWidget,
        "Bundled Upgrade": BundledStrategy,
        "Conditional Upgrade": ConditionalUpgradeWidget,
        # "Destruction Upgrade": None,
        "Incremental Upgrade": IncrementalUpgrade,
        "Influenced Upgrade": InfluencedUpgradeWidget,
        "Random Upgrade": RandomUpgradeWidget,
        # "Resetter Upgrade": None
    }
    return strategies
