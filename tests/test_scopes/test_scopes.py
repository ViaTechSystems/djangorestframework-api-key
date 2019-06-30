import pytest
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError

from rest_framework_api_key.models import APIKey, Scope

from ..project.heroes.models import Hero, HeroAPIKey

pytestmark = pytest.mark.django_db


def create_api_key() -> APIKey:
    api_key, _ = APIKey.objects.create_key(name="test")
    return api_key


def create_hero_api_key() -> HeroAPIKey:
    hero = Hero.objects.create(name="Batman")
    api_key, _ = HeroAPIKey.objects.create_key(name="test", hero=hero)
    return api_key


@pytest.fixture(name="api_key", params=[create_api_key, create_hero_api_key])
def fixture_api_key(request) -> APIKey:
    factory = request.param
    return factory()


def test_default_scopes(api_key):
    assert api_key.get_scopes() == set()


def test_builtin_scopes_created(hero_content_type: ContentType):
    scopes = list(Scope.objects.values_list("content_type", "code"))
    expected_scopes = {
        (hero_content_type.pk, "read"),
        (hero_content_type.pk, "create"),
        (hero_content_type.pk, "update"),
        (hero_content_type.pk, "delete"),
    }
    assert expected_scopes.issubset(set(scopes))


def test_custom_scopes_created(hero_content_type: ContentType):
    Scope.objects.get(content_type=hero_content_type, code="retire")


def test_create_scope(hero_content_type: ContentType):
    hero_call = Scope.objects.create(
        content_type=hero_content_type, code="call", name="Can call hero"
    )
    assert hero_call in Scope.objects.all()


def test_duplicate_scope(hero_read: Scope):
    with pytest.raises(IntegrityError):
        Scope.objects.create(
            content_type=hero_read.content_type, code=hero_read.code
        )


def test_label(hero_read: Scope):
    assert hero_read.label == "heroes.hero.read"


def test_str(hero_read: Scope):
    assert str(hero_read) == "heroes.hero.read"


def test_get_from_label(hero_read: Scope):
    assert Scope.objects.get_from_label("heroes.hero.read") == hero_read


def test_add_scope(api_key, hero_read: Scope):
    api_key.scopes.add(hero_read)
    assert api_key.get_scopes() == {"heroes.hero.read"}


@pytest.mark.parametrize(
    "factory, related_name, prefix_query",
    [
        (create_api_key, "apikey_set", "apikey__prefix"),
        (
            create_hero_api_key,
            "heroes_heroapikey_set",
            "heroes_heroapikey__prefix",
        ),
    ],
)
def test_related_queries(
    factory, related_name: str, prefix_query: str, hero_read: Scope
):
    api_key = factory()
    api_key.scopes.add(hero_read)
    assert list(getattr(hero_read, related_name).all()) == [api_key]
    assert list(Scope.objects.filter(**{prefix_query: api_key.prefix})) == [
        hero_read
    ]
