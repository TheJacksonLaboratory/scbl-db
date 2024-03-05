from pathlib import Path

from pytest import mark, raises, skip

import scbl_db.models.entities
from scbl_db.bases import Entity
from scbl_db.models.entities import *


# TODO: add more tests for each possible error
class TestInstitution:
    """
    Tests for the `Institution` model.
    """

    ror_id = '02der9h97'
    email_format = '{first_name}.{last_name}@uconn.edu'

    def test_ror_id_no_info(self):
        """
        Test that given a correct ROR ID, the model retrieves and sets
        sets the correct data from ROR.
        """
        institution = Institution(ror_id=self.ror_id, email_format=self.email_format)

        assert institution.ror_id == self.ror_id
        assert institution.email_format == self.email_format
        assert institution.name == 'University of Connecticut'
        assert institution.short_name == 'UConn'
        assert institution.country == 'US'
        assert institution.state == 'CT'
        assert institution.city == 'Storrs'

    def test_ror_id_with_info(self):
        """
        Test that given a correct ROR ID and user-given data, the model
        does not overwrite the user-given data.
        """
        name = 'Institution'
        short_name = 'INST'
        institution = Institution(
            ror_id=self.ror_id,
            email_format=self.email_format,
            name=name,
            short_name=short_name,
        )

        assert institution.name == name
        assert institution.short_name == short_name

    def test_nonexistent_ror_id(self):
        """
        Test that given a nonexistent ROR ID, the `Institution` model
        throws an error.
        """
        with raises(ValueError):
            Institution(ror_id='nonexistent_ror-id', email_format=self.email_format)

    def test_email_format_invalid_attribute(self):
        """
        Test that given an incorrect email format, the `Institution`
        model throws an error.
        """
        with raises(ValueError):
            Institution(
                ror_id=self.ror_id, email_format=r'{non_existent_attribute}@jax.org'
            )

    def test_email_format_no_variables(self):
        with raises(ValueError):
            Institution(ror_id=self.ror_id, email_format=r'contant_email@jax.org')


class TestPerson:
    """
    Tests for the `Person` model.
    """

    @mark.parametrize(argnames='n_dashes_to_remove', argvalues=range(1, 4))
    def test_orcid(self, person: Person, n_dashes_to_remove: int):
        """
        Test that the `Person` model accepts the ORCID, regardless of
        the number of dashes.
        """
        if person.orcid is None:
            skip('ORCID not set')

        new_person = Person(
            first_name=person.first_name,
            last_name=person.last_name,
            orcid=person.orcid.replace('-', '', n_dashes_to_remove),
            institution=person.institution,
        )

        assert new_person.orcid == person.orcid

    def test_invalid_orcid(self, person: Person):
        """
        Test that the `Person` model raises error with invalid ORCID.
        """
        with raises(ValueError):
            Person(
                first_name=person.first_name,
                last_name=person.last_name,
                orcid='invalid_orcid',
                institution=person.institution,
            )

    def test_nonexistent_orcid(self, person: Person):
        """
        Test that the `Person` model raises error with nonexistent ORCID.
        """
        with raises(ValueError):
            Person(
                first_name=person.first_name,
                last_name=person.last_name,
                orcid='9999-9999-9999-9999',
                institution=person.institution,
            )

    def test_email_autogenerated(self, person: Person):
        """
        Test that the `Person` model sets the email_auto_generated attribute
        to False when the email is given.
        """
        person = Person(
            first_name=person.first_name,
            last_name=person.last_name,
            institution=person.institution,
            email=person.email,
        )
        assert not person.email_auto_generated

    def test_autoset_email(self, person: Person):
        """
        Test that the `Person` model correctly sets the email attribute
        when given the minimum required information.
        """
        # Initialize a Person with a last name with a space
        person = Person(
            first_name=person.first_name,
            last_name='Said Alaani',
            institution=person.institution,
        )

        assert person.email == f'{person.first_name.lower()}.saidalaani@jax.org'
        assert person.email_auto_generated


class TestLab:
    """
    Tests for the `Lab` model.
    """

    def test_autoset_name(self, lab: Lab):
        """
        Test that the `Lab` model correctly sets the `name` attribute when
        given the minimum required information.
        """
        # This is kind of a dumb test
        assert lab.name == f'{lab.pi.first_name} {lab.pi.last_name} Lab'

    def test_autoset_delivery_dir(self, delivery_parent_dir: Path, lab: Lab):
        """
        Test that the `Lab` model correctly sets the `delivery_dir` and
        unix group automatically
        """
        assert lab.delivery_dir == str(
            delivery_parent_dir
            / f'{lab.pi.first_name.lower()}_{lab.pi.last_name.lower()}'
        )
        assert lab.unix_group == 'test_group'

    def test_invalid_delivery_dir(
        self, delivery_parent_dir: Path, institution: Institution, person: Person
    ):
        """
        Test that the `Lab` model raises an error when given an invalid
        delivery directory.
        """
        with raises(NotADirectoryError):
            Lab(institution=institution, pi=person, delivery_dir='invalid-directory')

    def test_nonexistent_autoset_delivery_dir(self, institution: Institution):
        """
        Test that the `Lab` model raises an error when the delivery
        directory is automatically set and does not exist.
        """
        different_person = Person(
            first_name='person', last_name='person', institution=institution
        )
        with raises(NotADirectoryError):
            Lab(institution=institution, pi=different_person)


@mark.parametrize(argnames='model_name', argvalues=scbl_db.models.entities.__all__)
def test_entities_are_Entity(model_name: str):
    """
    Test that all models in `scbl_db.models.entities` are subclasses of
    `Entity`.
    """
    model = getattr(scbl_db.models.entities, model_name)
    assert issubclass(model, Entity)
