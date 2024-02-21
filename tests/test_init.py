class TestInit:
    def test_model_availability(self):
        import scbl_db as scbl_db
        import scbl_db.models.entities as entities
        import scbl_db.models.platforms.chromium as chromium
        import scbl_db.models.platforms.xenium as xenium
        import scbl_db.models.processes as processes

        all_models = set(
            entities.__all__ + chromium.__all__ + xenium.__all__ + processes.__all__
        )
        assert all_models == scbl_db.ORDERED_MODELS.keys()
