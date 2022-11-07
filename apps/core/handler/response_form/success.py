def json_format(code, message, data):
    json_data = {
        'code': code,
        'message': message,
        'data': data
    }
    return json_data


def json_success(code, data):
    success_json = {}
    if code == 'S0001':
        success_json = json_format('S0001', '정상적으로 생성(Create) 되었습니다.', data)
        return success_json
    elif code == 'S0002':
        success_json = json_format('S0002', '정상적으로 수정(Update) 되었습니다.', data)
        return success_json
    elif code == 'S0003':
        success_json = json_format('S0003', '정상적으로 삭제(Delete) 되었습니다.', data)
        return success_json
    elif code == 'S0004':
        success_json = json_format('S0004', '정상적으로 처리 되었습니다.', data)
        return success_json
    elif code == 'S0006':
        success_json = json_format('S0006', '이미 저장된 데이터가 있습니다.', data)
        return success_json
    elif code == 'S0007':
        success_json = json_format('S0007', '유효한 접근 토큰(Access Token)입니다.', data)
        return success_json
    elif code == 'S0008':
        success_json = json_format('S0008', '로그인(Login) 성공', data)
        return success_json
    elif code == 'S0009':
        success_json = json_format('S0009', '회원가입(SignUp) 성공', data)
        return success_json
    elif code == 'S0010':
        success_json = json_format('S0010', '올바른 인증 번호(Cert Number)입니다.', data)
        return success_json
    elif code == 'E9999':
        success_json = json_format('E9999', '요청(Request)이 올바르지 않습니다.', data)
        return success_json
    else:
        success_json = json_format(code, '정상적으로 처리 되었습니다.', data)
        return success_json
