"""Base model."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.collections import InstrumentedList

from api.helpers.general import is_substring

# pylint:disable=no-member, invalid-name, broad-except, no-else-return

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base model with all main requirements of a model."""

    __abstract__ = True

    def delete(self):
        """Delete an object from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return {
                "message": "Error encountered during deletion.",
                "help": "Ensure the database is running properly.",
                "exception": str(e)
            }

    def get_field(self, field):
        """Get the value in an object's field."""
        try:
            values = getattr(self, field)
            return values
        except AttributeError:
            return {
                "message": "Ensure the  field passed is valid.",
                "help": "The field should be an attribute of the object."
            }

    def insert(self, field, *values):
        """Insert values into a relationship field."""
        current_values = self.get_field(field)
        if isinstance(current_values, dict):
            return current_values
        elif isinstance(current_values, InstrumentedList):
            try:
                current_values.extend(list(values))
            except Exception as e:
                return {
                    "message": "Ensure the values you're inserting are valid.",
                    "help": "The objects should relate to the inserted field.",
                    "exception": str(e)
                }
            self.save()
        try:
            setattr(self, field, values[0])
        except Exception as e:
            return {
                "message": "Ensure the values you're inserting are valid.",
                "help": "The objects should relate to the inserted field.",
                "exception": str(e)
            }
        self.save()

    def remove(self, field, **kwargs):
        """
        Remove values from a relationship field.

        This replaces the value with None or an empty list.
        Pass in the field and unique argument to isolate object for removal.
        """
        current_values = self.get_field(field)
        if isinstance(current_values, dict):
            return current_values
        elif isinstance(current_values, InstrumentedList):
            if kwargs:
                key = [i for i in kwargs][0]
                try:
                    item_index = current_values.index([
                        i for i in current_values
                        if getattr(i, key) == kwargs[key]
                    ][0])
                    current_values.pop(item_index)
                except Exception as e:
                    return {
                        "message": "Ensure the arguments passed are valid.",
                        "help": "Should be of an existent object and unique.",
                        "exception": str(e)
                    }
            else:
                setattr(self, field, InstrumentedList([]))
        else:
            setattr(self, field, None)
        self.save()

    def save(self):
        """Save an object in the database."""
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            db.session.rollback()
            return {
                "message": "Ensure the object you're saving is valid",
                "help": "Has all fields and doesn't repeat unique values.",
                "exception": str(e)
            }

    def serialize(self):
        """Convert sqlalchemy object to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def update(self, new_data):
        """Update an object with new information."""
        all_keys = [key for key in self.__dict__]
        keys = [key for key in new_data]
        for key in keys:
            if key in all_keys:
                setattr(self, key, new_data[key])
            else:
                return {
                    "message": "Error encountered when setting attributes.",
                    "help": "Ensure all fields you're updating are valid."
                }
        self.save()

    @classmethod
    def check_exists(cls, **kwargs):
        """Check whether an object exists in the database."""
        return bool(cls.query.filter_by(**kwargs).first())

    @classmethod
    def drop(cls):
        """Delete all objects of a table."""
        objects = cls.get_all()
        if isinstance(objects, dict) is False:
            for i in cls.get_all():
                i.delete()
            return True
        else:
            return True

    @classmethod
    def get(cls, **kwargs):
        """Get a specific object from the database."""
        result = cls.query.filter_by(**kwargs).first()
        if not result:
            return {
                "message": "The object does not exist",
                "help": "Ensure arguments are of existent objects and unique."
            }
        return result

    @classmethod
    def get_all(cls):
        """Get all objects of a specific table."""
        result = cls.query.all()
        if not result:
            return {
                "message": "The class of objects do not exist",
                "help": "Ensure the class required has objects."
            }
        return result

    @classmethod
    def search(cls, **kwargs):
        """Search through values of string fields."""
        key = [key for key in kwargs][0]
        objects = cls.get_all()
        if isinstance(objects, dict):
            return objects
        results = []
        for i in objects:
            if is_substring(kwargs[key], getattr(i, key)):
                results.append(i)
        if not results:
            return {
                "message": "No objects match the searched value.",
                "help": "Ensure arguments are of existent objects."
            }
        return results
