from api.helpers.auth import view_token
from api.helpers.validation import validate_json
from api.models import Board, Estate, Role, Unit, User


def get_boards(board_id=None):
    """
    Get board(s).
    """
    if board_id:
        board = Board.get(id=board_id)
        if isinstance(board, dict):
            return {
                'status': 'fail',
                'message': 'The board does not exist.',
                'help': 'Ensure board_id is of an existent board.'
            }
        else:
            return board
    else:
        boards = Board.get_all()
        if isinstance(boards, dict):
            return {
                'status': 'fail',
                'message': 'No boards exist.',
                'help': 'Add boards to the database.'
            }
        else:
            return boards


def get_conversations(request, conversation_id=None):
    """
    Get conversation(s) of a user.
    """
    user = User.get(id=view_token(
        request.headers.get('Authorization'))['id'])
    conversations = user.conversations
    if conversations:
        if conversation_id:
            try:
                conversation = [conversation for conversation in conversations
                                if conversation.id == conversation_id][0]
                return conversation
            except IndexError:
                return {
                    'status': 'fail',
                    'message': 'The conversation does not exist.',
                    'help': 'Ensure conversation_id is existent.'
                }
        else:
            return conversations
    else:
        return {
            'status': 'fail',
            'message': 'The user has no conversations.',
            'help': 'Open at least one conversation.'
        }


def get_estates(estate_id=None):
    """
    Get estate(s).
    """
    if estate_id:
        estate = Estate.get(id=estate_id)
        if isinstance(estate, dict):
            return {
                'status': 'fail',
                'message': 'The estate does not exist.',
                'help': 'Ensure estate_id is of an existent estate.'
            }
        else:
            return estate
    else:
        estates = Estate.get_all()
        if isinstance(estates, dict):
            return {
                'status': 'fail',
                'message': 'No estates exist.',
                'help': 'Add estates to the database.'
            }
        else:
            return estates


def get_messages(request, conversation_id, message_id=None):
    conversation = get_conversations(request, conversation_id)
    if isinstance(conversation, dict):
        return conversation
    else:
        if message_id:
            try:
                message = [
                    message for message in conversation.messages
                    if message.id == message_id][0]
                return message
            except IndexError:
                return {
                    'status': 'fail',
                    'message': 'The message does not exist.',
                    'help': 'Ensure message_id is existent.'
                }
        else:
            if conversation.messages:
                return conversation.messages
            else:
                return {
                    'status': 'fail',
                    'message': 'The conversation has no messages.',
                    'help': 'Send at least one message.'
                }


def get_roles(role_id=None):
    """
    Get role(s).
    """
    if role_id:
        role = Role.get(id=role_id)
        if isinstance(role, dict):
            return {
                'status': 'fail',
                'message': 'The role does not exist.',
                'help': 'Ensure role_id is existent.'
            }
        else:
            return role
    else:
        roles = Role.get_all()
        if isinstance(roles, dict):
            return {
                'status': 'fail',
                'message': 'There are no roles in the system.',
                'help': 'Ensure roles are seeded.'
            }
        else:
            return roles


def get_units(unit_id=None):
    """
    Get unit(s).
    """
    if unit_id:
        unit = Unit.get(id=unit_id)
        if isinstance(unit, dict):
            return {
                'status': 'fail',
                'message': 'The unit does not exist.',
                'help': 'Ensure unit_id is existent.'
            }
        else:
            return unit
    else:
        units = Unit.get_all()
        if isinstance(units, dict):
            return {
                'status': 'fail',
                'message': 'There are no units in the system.',
                'help': 'Add some units if necessary.'
            }
        else:
            return units


def get_user(request, user_id=None):
    """
    Get user(s).
    """
    if user_id:
        user = User.get(id=user_id)
        if isinstance(user, dict):
            return {
                'status': 'fail',
                'message': 'The user does not exist.',
                'help': 'Ensure arguments are of existent object.'
            }
        else:
            return user
    else:
        user = User.get(id=view_token(
            request.headers.get('Authorization'))['id'])
        if isinstance(user, dict):
            return {
                'status': 'fail',
                'message': 'The user does not exist.',
                'help': 'Ensure arguments are of existent object.'
            }
        else:
            return user


def get_users():
    users = User.get_all()
    if isinstance(users, dict):
        return {
            'status': 'fail',
            'message': 'There are no users in the database.',
            'help': 'Ensure there are some users in the database'}
    else:
        return {
            'status': 'success',
            'data': {
                'users': [user.__repr__() for user in users]
            }
        }


def search_users(name):
    users = User.search(name=name)
    if isinstance(users, dict) is False:
        return {
            'status': 'success',
            'data': {
                'users': [user.__repr__() for user in users]
            }
        }
    else:
        return {
            'status': 'fail',
            'message': 'No users with the name in the database.',
            'help': 'Try searching with another name.'
        }


def update_resource(request, resource):
    payload = request.get_json()
    val_result = validate_json(['new_data'], payload)
    if isinstance(val_result, bool) is True:
        update_result = resource.update(payload['new_data'])
        if isinstance(update_result, dict):
            return update_result
        else:
            return True
    else:
        return {
            'status': 'fail',
            'message': 'Not all fields were provided.',
            'missing': val_result
        }
