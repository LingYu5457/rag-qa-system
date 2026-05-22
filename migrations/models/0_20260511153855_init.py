from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `user` (
    `user_id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    `user_name` VARCHAR(50) NOT NULL COMMENT '用户名',
    `user_account` VARCHAR(50) NOT NULL UNIQUE COMMENT '登录账号',
    `user_password` VARCHAR(255) NOT NULL COMMENT '密码(加密存储)',
    `is_delete` BOOL NOT NULL COMMENT '逻辑删除：0-未删除，1-已删除' DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    KEY `idx_user_is_dele_f221b4` (`is_delete`)
) CHARACTER SET utf8mb4 COMMENT='用户表';
CREATE TABLE IF NOT EXISTS `session` (
    `session_id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '会话ID',
    `session_title` VARCHAR(100) NOT NULL COMMENT '会话标题' DEFAULT '新对话',
    `is_delete` BOOL NOT NULL COMMENT '逻辑删除：0-未删除，1-已删除' DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `user_id` BIGINT NOT NULL COMMENT '关联用户',
    CONSTRAINT `fk_session_user_8f5e6599` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    KEY `idx_session_is_dele_3d96b5` (`is_delete`),
    KEY `idx_session_user_id_23ddbc` (`user_id`)
) CHARACTER SET utf8mb4 COMMENT='会话表';
CREATE TABLE IF NOT EXISTS `chat` (
    `chat_id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '消息ID',
    `role` VARCHAR(20) NOT NULL COMMENT '角色：system/ai/human',
    `chat_message` LONGTEXT NOT NULL COMMENT '消息内容',
    `is_delete` BOOL NOT NULL COMMENT '逻辑删除：0-未删除，1-已删除' DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `session_id` BIGINT NOT NULL COMMENT '关联会话',
    CONSTRAINT `fk_chat_session_e7c14d97` FOREIGN KEY (`session_id`) REFERENCES `session` (`session_id`) ON DELETE CASCADE,
    KEY `idx_chat_is_dele_ec36e4` (`is_delete`),
    KEY `idx_chat_session_aadf62` (`session_id`)
) CHARACTER SET utf8mb4 COMMENT='聊天消息表';
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmltz2joQx78Kw1M604sxyDbnDRLSctqEMwk5p9Om45FtGTzxhdpyE6aT735WwsZ3MO"
    "USMsMLA9KuLP92Jf3X5nfT8QxiB+/Pp5g2/2r8brrYIfAl0/620cSzWdLKGijWbG6oxxZa"
    "QH2ss1FMbAcEmgwS6L41o5bnMsv7UBE6+D5EXbF7H0qGosCnIJnQrkgKG8PwdBjEcif1zE"
    "PX+hkSlXoTQqfEB6fvP6DZcg3yRIL45+xBNS1iG5nbY7NWLYONwjtVOp/xjr41Gbr0kjuw"
    "GWmq7tmh4+acZnM69dyll+VyBhPiEh9Twq5F/ZAxcEPbjlDFWBbTTkwW8035GMTEoc1IMu"
    "8ykAmN4UUeXOSjey4LCMws4Hc+YVd81xXFdlsWhbakoI4sI0VQwJZPr9glPy8IJIQWQ3FO"
    "w4/D6zG7tgdRX6QCa3jmPpjihRePQoLd98CywBySzC8nHtvncMON5XHHcFfxjhsS4Emmri"
    "OudA0RPkUZPk2zhYN5QInzAVsfpqGD3ZpBcPCTahN3QqfwUxRW8P23d3P+qXdzJgpvspCv"
    "ox6RdzHcuax2SBDgSQnmMXlaldgpv5fHnV7uqKUg+NS0bj3KK6iOB195zjpB8NNO0zy76n"
    "3loJ151PNldP0xNk/RP/8y6ueoW4EKuyKhJcj7HiQwdsupZ/xyyDVw3A3zwp5SuTt3hbYG"
    "KW52W0BbFAVokaTOIt2FdxANWcT5HkFvQQ8yTDHds3Wc+qPRl0yc+sN8IO6u+oObsxYPGh"
    "hZNLMFpdaETxg/dXFKZcNzAT3UckjFqsh45gJkRK7v4y+HXiFIbEG0ENhBZJApAXlk1iTf"
    "hDszRq49j/Jj1YoZXg1ux72rfzLhuOiNB6xHzCyZuPVMyu1Zy0Ea/w3HnxrsZ+Pb6HrAuX"
    "oBnfj8iond+FuTzQmH1FNd71HFRiqV49YYVybcAexiwGjjsz3rt/5439FirIxuS24zAYRg"
    "lXVg/cF3zTCO7ahn8sp8KD3pI57FIFx6PrEm7mcy54EYwtSxq5ftgZEEvU1GeiUBeI6TK2"
    "5NLuzjx6UazeUcfImOAyaJerfnvYtBkyPWsP7wiH1DzbBmPZ7o5VqWtsUuR3TyLdiFE9+I"
    "boRNO8e8pCJIhaO6KEhFv05dkACurAXKTLbQ/4faJvZaBSRMXlcVEEOkFt2sHCg4Hk6oMk"
    "2KNIHpULOb2gxWpbIE8OBYVrqFhK5THrSEOvUBWFUWCLzvpFVPWvWkVY9Sq4YB8Tc+gVJO"
    "R6VSZSSyil1sy8d2FK1QqQzmDiTqXTTMK0FfV5+mUm1TcZp9JhWUpHjkdvn5htiYRmKxHG"
    "/8EPqgW9Ye9P/zPiU7z8ESvR7nZrVYjxdBHaWepFqlUi8z2UKp73+T3KtGT2i8Lo3OCfIf"
    "G+jzjNPLP0ROZyLqCHUfn2RUOKojwlG1BkcFCc4hYV33QrdE5q2Bm/LbDd8tMluSmagzEY"
    "J1bogg6lDbrHv4H4LxDAfBo+eXbB1rIKcdXz6LkaYDW1kRWmdMSWMhbkIagvRGAlbe/NHr"
    "J4TqvH9CqPoFFOs71Zen+vJUXx5NfVkodupo9Oi52pYyfacP6v9Mqe+qEtqrUu8R39KnzR"
    "KtHvWsVOs4sVmn12NiRQxb6PEyKV6pw19eglczKJfdYqsjd5S21Fmq7WXLKpG9XlD/In75"
    "C7FqMZJyeWEZUp/i/iUGWxobQIzMXyfAvbwDgCtSUlZ7/H07uq44/hOXHMg7F27wu2Hp9G"
    "3DtgL64zixrqDI7jpzoBf+E5T/+0/upGYD9MueMx7y3e3z/61EOKQ="
)
