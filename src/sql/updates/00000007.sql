
ALTER TABLE tree MODIFY COLUMN PARENT BIGINT(20) UNSIGNED;

ALTER TABLE tree ADD CONSTRAINT `childToParent` FOREIGN KEY (parent) REFERENCES tree (inode) ON DELETE CASCADE ON UPDATE CASCADE;

