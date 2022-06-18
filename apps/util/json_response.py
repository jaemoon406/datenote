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


def json_error(code):
    error_json = {}
    if code == 'E0001':
        error_json = json_format('E0001', '고유 키(main-key)값이 올바르지 않습니다.', None)
        return error_json
    elif code == 'E0002':
        error_json = json_format('E0002', '키(key)값이 올바르지 않습니다.', None)
        return error_json
    elif code == 'E0003':
        error_json = json_format('E0003', '밸류(value)값이 올바르지 않습니다.', None)
        return error_json
    elif code == 'E0004':
        error_json = json_format('E0004', '헤더(Header)의 인증 키가 올바르지 않습니다.', None)
        return error_json
    elif code == 'E0005':
        error_json = json_format('E0005', '로그인 실패', None)
        return error_json
    elif code == 'E0006':
        error_json = json_format('E0006', '메소드(Method)가 올바르지 않습니다.', None)
        return error_json
    elif code == 'E0007':
        error_json = json_format('E0007', '중복되는 이메일(email)이 존재합니다.', None)
        return error_json
    elif code == 'E0008':
        error_json = json_format('E0008', '중복되는 아이디(username)이 존재합니다.', None)
        return error_json
    elif code == 'E0010':
        error_json = json_format('E0010', '서버에 요청과 일치하는 데이터가 없습니다.', None)
        return error_json
    elif code == 'E0011':
        error_json = json_format('E0011', '접근 토큰(Access Token)의 갱신이 필요합니다.', None)
        return error_json
    elif code == 'E0012':
        error_json = json_format('E0012', '인증 번호(Cert Number)가 올바르지 않습니다.', None)
        return error_json
    elif code == 'E0013':
        error_json = json_format('E0013', '유저(User) 정보가 존재하지 않습니다.', None)
        return error_json
    elif code == 'E0014':
        error_json = json_format('E0014', '아이디(Username)가 규격에 맞지 않습니다.', None)
        return error_json
    elif code == 'E0015':
        error_json = json_format('E0015', '닉네임(Nickname)이 규격에 맞지 않습니다.', None)
        return error_json
    elif code == 'E0017':
        error_json = json_format('E0017', '데이터(Data)의 자리수가 규격을 초과했습니다.', None)
        return error_json
    elif code == 'E0404':
        error_json = json_format('E0404', '주소(URL)가 올바르지 않습니다.', None)
        return error_json
    elif code == 'E0403':
        error_json = json_format('E0403', '접근 권한이 없습니다.', None)
        return error_json
    elif code == 'E0400':
        error_json = json_format('E0400', '요청(Request)이 올바르지 않습니다.', None)
        return error_json
    elif code == 'E0500':
        error_json = json_format('E0500', '서버(Server)에 문제가 있습니다.', None)
        return error_json
    elif code == 'E1005':
        error_json = json_format('E1005', '페이지가 존재하지 않습니다', None)
        return error_json

