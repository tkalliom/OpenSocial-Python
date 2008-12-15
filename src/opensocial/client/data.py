import logging

def extract_fields(json):
  """Extracts a JSON dict of fields.
  
  REST and RPC protocols use different JSON keys for OpenSocial objects. This
  abstracts that and handles both cases.
  
  Args:
    json: dict The JSON object.
  
  Returns: A JSON dict of field/value pairs.
  """
  return json.get('data') or json.get('entry') or {}   


class Object(object):
  """Generic container for opensocial.* objects.
  """

  def __init__(self, fields):
    self.fields = fields

  def get_field(self, name):
    """Retrieves a specific field value for this Object.
    
    Returns: The field value.
    """ 
    return self.fields.get(name)


class Person(Object):
  """An opensocial.Person representation.
  """

  def __init__(self, fields):
    super(Person, self).__init__(fields)

  def get_id(self):
    """Returns the id of this Person.
    
    Returns: The container-specific id of this Person.
    """ 
    return self.get_field('id')
      
  def get_display_name(self):
    """Returns the full name of this Person.
    
    Returns: The full name of this Person.
    """ 
    names = self.get_field('name')
    if names:
      return '%s %s' % (names['givenName'], names['familyName'])
    else:
      return ''

  @staticmethod
  def parse_json(json):
    """Creates a Person object from a JSON dict of fields.
    Args:
      json: dict The Person fields.
      
    Returns: A Person object.      
    """
    return Person(extract_fields(json))


class Collection(object):
  """Contains a collection of OpenSocial objects.
  
  Handles the parsing of a JSON object and creation of the associated OpenSocial
  data object.
  """
  
  def __init__(self, items, start, total):
    self.items = items
    self.start = start
    self.total = total
  
  @staticmethod
  def parse_json(json, cls):
    """Creates a collection from a JSON object returned by an OpenSocial
    container.
    
    Args:
      json: dict The JSON object.
      cls: The OpenSocial data type to instantiate for each entry in the
           collection.
    
    Returns: A Collection of OpenSocial objects.
    """
    start = json.get('startIndex')
    total = json.get('totalResults')
    items = []
    json_list = json.get('entry')
    for fields in json_list:
      items.append(cls(fields))
    return Collection(items, start, total)