from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `file` ADD `chat_id` BIGINT COMMENT '关联聊天消息（记录在chat里的位置）';
        ALTER TABLE `file` ADD `is_rag` BOOL NOT NULL COMMENT '是否为RAG文件' DEFAULT 0;
        ALTER TABLE `file` ADD CONSTRAINT `fk_file_chat_36a2a6e8` FOREIGN KEY (`chat_id`) REFERENCES `chat` (`chat_id`) ON DELETE CASCADE;
        ALTER TABLE `file` ADD INDEX `idx_file_chat_id_77ae35` (`chat_id`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `file` DROP INDEX `idx_file_chat_id_77ae35`;
        ALTER TABLE `file` DROP FOREIGN KEY `fk_file_chat_36a2a6e8`;
        ALTER TABLE `file` DROP COLUMN `chat_id`;
        ALTER TABLE `file` DROP COLUMN `is_rag`;"""


MODELS_STATE = (
    "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"
)
