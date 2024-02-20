from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

import scbl_db.models.entities as entities
import scbl_db.models.platforms.chromium as chromium_module
import scbl_db.models.platforms.xenium as xenium_module
import scbl_db.models.processes as processes
from scbl_db.models.entities import *
from scbl_db.models.platforms.chromium import *
from scbl_db.models.platforms.xenium import *
from scbl_db.models.processes import *

from .db_fixtures import tmp_db_session
from .test_models.model_instance_fixtures import *


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
        xenium_sample: XeniumSample,
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
            for module in [
                xenium_module,
                chromium_module,
                entities,
                processes,
            ]:
                for model_name in module.__all__:
                    model = getattr(module, model_name)
                    assert session.execute(select(model)).scalar() is not None
