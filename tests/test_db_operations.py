from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from scbl_db import *

from .test_models.conftest import *


class TestDBInsert:
    """
    Tests that verify instances of models can be inserted into the
    database.
    """

    def test_insert(
        self,
        tmp_db_session: sessionmaker[Session],
        institution: Institution,
        person: Person,
        lab: Lab,
        chromium: Platform,
        xenium: Platform,
        chromium_assay: Assay,
        xenium_assay: Assay,
        chromium_data_set: ChromiumDataSet,
        chromium_sample: ChromiumSample,
        chromium_library_type: ChromiumLibraryType,
        sequencing_run: SequencingRun,
        chromium_library: ChromiumLibrary,
        chromium_tag: ChromiumTag,
        xenium_run: XeniumRun,
        xenium_data_set: XeniumDataSet,
        xenium_sample: XeniumRegion,
    ):
        """
        Verify that instances of models can be inserted into the database.
        """
        with tmp_db_session.begin() as session:
            session.add(institution)
            session.add(person)
            session.add(lab)
            session.add(chromium)
            session.add(xenium)
            session.add(chromium_assay)
            session.add(xenium_assay)
            session.add(chromium_data_set)
            session.add(chromium_tag)
            session.add(chromium_sample)
            session.add(chromium_library_type)
            session.add(sequencing_run)
            session.add(chromium_library)
            session.add(xenium_run)
            session.add(xenium_data_set)
            session.add(xenium_sample)

        with tmp_db_session.begin() as session:
            for model in ORDERED_MODELS.values():
                assert session.execute(select(model)).scalar() is not None
