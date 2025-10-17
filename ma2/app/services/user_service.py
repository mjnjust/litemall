# 在这个简化版本中，服务层可以直接在路由中实现
# 但如果业务逻辑复杂，可以将其提取到服务层

class UserService:
    @staticmethod
    def validate_user_data(data):
        errors = []

        if not data.get('username'):
            errors.append('Username is required')
        elif len(data.get('username', '')) < 3:
            errors.append('Username must be at least 3 characters')

        if not data.get('email'):
            errors.append('Email is required')
        elif '@' not in data.get('email', ''):
            errors.append('Email must be valid')

        return errors

    @staticmethod
    def format_user_response(user):
        # 可以在这里格式化响应数据
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'profile_url': f"/api/users/{user['id']}"
        }