"""密码单向哈希与验证工具。

本模块使用 PBKDF2-HMAC-SHA256 将明文密码转换为不可逆的密码哈希。
密码不会被加密或解密：登录验证时使用原密码、已保存的随机盐和迭代次数
重新计算摘要，再与数据库中的摘要进行安全比较。

数据库保存格式：
    pbkdf2_sha256$迭代次数$Base64随机盐$Base64摘要

随机盐使相同密码产生不同哈希；高迭代次数提高暴力破解的计算成本。
"""

import base64
import hashlib
import hmac
import secrets


class PasswordHasher:
    """封装 PBKDF2 密码哈希生成和验证逻辑。"""

    # 哈希字符串中的算法标识，用于验证时识别存储格式。
    ALGORITHM = "pbkdf2_sha256"
    # PBKDF2 重复计算次数，数值越高，暴力尝试单个密码的成本越高。
    ITERATIONS = 600_000
    # 每个密码使用 16 字节加密安全随机盐，防止相同密码产生相同哈希。
    SALT_SIZE = 16

    def hash(self, password: str) -> str:
        """生成可保存到数据库的自描述密码哈希字符串。

        算法流程：
        1. 使用 secrets 生成不可预测的随机盐。
        2. 将密码按 UTF-8 编码为字节。
        3. 使用 PBKDF2-HMAC-SHA256 迭代计算密码摘要。
        4. 将二进制盐和摘要编码为 Base64 文本。
        5. 将算法、迭代次数、盐和摘要组合成一个字符串。

        同一密码每次都会使用新的随机盐，因此生成结果不会相同。
        """
        salt = secrets.token_bytes(self.SALT_SIZE)
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, self.ITERATIONS
        )
        encoded_salt = base64.b64encode(salt).decode("ascii")
        encoded_digest = base64.b64encode(digest).decode("ascii")
        return (
            f"{self.ALGORITHM}${self.ITERATIONS}$"
            f"{encoded_salt}${encoded_digest}"
        )

    def verify(self, password: str, stored_hash: str) -> bool:
        """验证明文密码是否与已保存的哈希匹配。

        方法会解析存储字符串，恢复迭代次数和随机盐，再用输入密码重新计算
        摘要。最终使用 hmac.compare_digest 进行恒定时间比较，降低通过比较
        耗时推测摘要内容的风险。格式损坏或算法不匹配时直接返回 False。
        """
        try:
            algorithm, iterations, encoded_salt, encoded_digest = (
                stored_hash.split("$", 3)
            )
            if algorithm != self.ALGORITHM:
                return False

            salt = base64.b64decode(encoded_salt, validate=True)
            expected_digest = base64.b64decode(encoded_digest, validate=True)
            actual_digest = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt, int(iterations)
            )
        except (TypeError, ValueError):
            return False

        return hmac.compare_digest(actual_digest, expected_digest)
