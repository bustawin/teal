from typing import Dict, Set, Type

from boltons.typeutils import issubclass
from boltons.urlutils import URL

from teal.resource import Resource


class Config:
    """
    The configuration class.

    Subclass and set here your config values.
    """
    RESOURCE_DEFINITIONS = set()  # type: Set[Type[Resource]]
    """
    A list of resource definitions to load.
    """

    SQLALCHEMY_DATABASE_URI = None  # type: str
    """
    The access to the main Database.
    """
    SQLALCHEMY_BINDS = {}  # type: Dict[str, str]
    """
    Optional extra databases. See `here <http://flask-sqlalchemy.pocoo.org
    /2.3/binds/#referring-to-binds>`_ how bind your models to different
    databases.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    """
    Disables flask-sqlalchemy notification system. 
    Save resources and hides a warning by flask-sqlalchemy itself.
    
    See `this answer in Stackoverflow for more info
    <https://stackoverflow.com/a/33790196>`_. 
    """

    SCHEMA = None  # type: str
    """
    A string describing the main PostgreSQL's schema. ``None`` disables
    this functionality.
    
    If you use a factory of apps (for example by using
    :func:`teal.teal.prefixed_database_factory`) and then set this
    value differently per each app (as each app has a separate config)
    you effectively create a `multi-tenant app <https://
    news.ycombinator.com/item?id=4268792>`_.
    
    Your models by default will be created in this ``SCHEMA``,
    unless you set something like::
    
        class User(db.Model):
            __table_args__ = {'schema': 'users'}
            
    In which case this will be created in the ``users`` schema.
    
    Schemas are interesting over having multiple databases (i.e. using
    flask-sqlalchemy's data binding) because you can have relationships
    between them.
    
    Note that this only works with PostgreSQL.
    """

    API_DOC_CONFIG_TITLE = 'Teal'
    API_DOC_CONFIG_VERSION = '0.1'
    """
    Configuration options for the api docs. They are the parameters
    passed to `apispec <http://apispec.readthedocs.io/en/
    latest/api_core.html#apispec.APISpec>`_. Prefix the configuration
    names with ``API_DOC_CONFIG_``.
    """
    API_DOC_CLASS_DISCRIMINATOR = None
    """
    Configuration options for the api docs class definitions.
    
    You can pass any `schema definition <https://github.com/OAI/
    OpenAPI-Specification/blob/master/versions/2.0.md#schemaObject>`_
    prefiex by ``API_DOC_CLASS_`` like in the example above.
    """

    CORS_ORIGINS = '*'
    CORS_EXPOSE_HEADERS = 'Authorization'
    CORS_ALLOW_HEADERS = 'Content-Type', 'Authorization'
    """
    Configuration for CORS. See the options you can pass by in `Flask-Cors 
    <https://flask-cors.corydolphin.com/en/latest/api.html#extension>`_,
    exactly in **Parameters**, like the ones above.
    """

    def __init__(self, db: str = None) -> None:
        """
        :param db: Optional. Set the ``SQLALCHEMY_DATABASE_URI`` param.
        """
        for r in self.RESOURCE_DEFINITIONS:
            assert issubclass(r, Resource), '{0!r} is not a subclass of Resource'.format(r)
        if db:
            assert URL(db), 'Set a valid URI'
            self.SQLALCHEMY_DATABASE_URI = db
