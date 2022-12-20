BEGIN;
--
-- Create model ParsingRule
--
CREATE TABLE "feed_parsingrule" ("id" bigserial NOT NULL PRIMARY KEY, "created" timestamp with time zone NOT NULL, "modified" timestamp with time zone NOT NULL);
--
-- Create model Feed
--
CREATE TABLE "feed_feed" ("id" bigserial NOT NULL PRIMARY KEY, "created" timestamp with time zone NOT NULL, "modified" timestamp with time zone NOT NULL, "type_of_feed" varchar(13) NOT NULL, "format_of_feed" varchar(15) NOT NULL, "auth_type" varchar(7) NOT NULL, "polling_frequency" varchar(17) NOT NULL, "auth_login" varchar(32) NULL, "auth_password" varchar(64) NULL, "auth_querystring" varchar(128) NULL, "separator" varchar(8) NULL, "custom_field" varchar(128) NULL, "sertificate" varchar(100) NULL, "vendor" varchar(32) NOT NULL, "name" varchar(32) NOT NULL UNIQUE, "link" varchar(255) NOT NULL, "confidence" integer NOT NULL, "records_quantity" integer NULL, "update_status" varchar(15) NOT NULL, "ts" timestamp with time zone NOT NULL, "source_id" bigint NULL);
CREATE TABLE "feed_feed_indicators" ("id" bigserial NOT NULL PRIMARY KEY, "feed_id" bigint NOT NULL, "indicator_id" bigint NOT NULL);
CREATE TABLE "feed_feed_parsing_rules" ("id" bigserial NOT NULL PRIMARY KEY, "feed_id" bigint NOT NULL, "parsingrule_id" bigint NOT NULL);
ALTER TABLE "feed_feed" ADD CONSTRAINT "feed_feed_source_id_9a5ec196_fk_source_source_id" FOREIGN KEY ("source_id") REFERENCES "source_source" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "feed_feed_name_91643a81_like" ON "feed_feed" ("name" varchar_pattern_ops);
CREATE INDEX "feed_feed_source_id_9a5ec196" ON "feed_feed" ("source_id");
ALTER TABLE "feed_feed_indicators" ADD CONSTRAINT "feed_feed_indicators_feed_id_indicator_id_2ab7aae4_uniq" UNIQUE ("feed_id", "indicator_id");
ALTER TABLE "feed_feed_indicators" ADD CONSTRAINT "feed_feed_indicators_feed_id_d404f0c0_fk_feed_feed_id" FOREIGN KEY ("feed_id") REFERENCES "feed_feed" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "feed_feed_indicators" ADD CONSTRAINT "feed_feed_indicators_indicator_id_af143cca_fk_indicator" FOREIGN KEY ("indicator_id") REFERENCES "indicator_indicator" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "feed_feed_indicators_feed_id_d404f0c0" ON "feed_feed_indicators" ("feed_id");
CREATE INDEX "feed_feed_indicators_indicator_id_af143cca" ON "feed_feed_indicators" ("indicator_id");
ALTER TABLE "feed_feed_parsing_rules" ADD CONSTRAINT "feed_feed_parsing_rules_feed_id_parsingrule_id_254f09ec_uniq" UNIQUE ("feed_id", "parsingrule_id");
ALTER TABLE "feed_feed_parsing_rules" ADD CONSTRAINT "feed_feed_parsing_rules_feed_id_9535246d_fk_feed_feed_id" FOREIGN KEY ("feed_id") REFERENCES "feed_feed" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "feed_feed_parsing_rules" ADD CONSTRAINT "feed_feed_parsing_ru_parsingrule_id_cbe28e6e_fk_feed_pars" FOREIGN KEY ("parsingrule_id") REFERENCES "feed_parsingrule" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "feed_feed_parsing_rules_feed_id_9535246d" ON "feed_feed_parsing_rules" ("feed_id");
CREATE INDEX "feed_feed_parsing_rules_parsingrule_id_cbe28e6e" ON "feed_feed_parsing_rules" ("parsingrule_id");
COMMIT;

BEGIN;
--
-- Alter field auth_type on feed
--
--
-- Alter field format_of_feed on feed
--
--
-- Alter field type_of_feed on feed
--
COMMIT;