from flask import current_app

def validate_password(password: str) -> tuple[bool, str]:
    """验证密码是否符合要求"""
    if len(password) < current_app.config['PASSWORD_MIN_LENGTH']:
        return False, f'密码长度必须不少于{current_app.config["PASSWORD_MIN_LENGTH"]}个字符'
        
    if current_app.config['PASSWORD_REQUIRE_UPPER'] and not any(c.isupper() for c in password):
        return False, '密码必须包含大写字母'
        
    if current_app.config['PASSWORD_REQUIRE_LOWER'] and not any(c.islower() for c in password):
        return False, '密码必须包含小写字母'
        
    if current_app.config['PASSWORD_REQUIRE_DIGITS'] and not any(c.isdigit() for c in password):
        return False, '密码必须包含数字'
        
    if current_app.config['PASSWORD_REQUIRE_SPECIAL'] and not any(c in '!@#$%^&*(),.?":{}|<>' for c in password):
        return False, '密码必须包含特殊字符'
        
    return True, '' 