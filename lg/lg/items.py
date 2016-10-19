# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LgJobItem(scrapy.Item):
    format_create_time = scrapy.Field()
    publisher_id = scrapy.Field()
    business_zones = scrapy.Field()
    create_time = scrapy.Field()
    company_id = scrapy.Field()
    position_name = scrapy.Field()
    education = scrapy.Field()
    city = scrapy.Field()
    position_id = scrapy.Field()
    finance_stage = scrapy.Field()
    company_short_name = scrapy.Field()
    company_logo = scrapy.Field()
    salary = scrapy.Field()
    salary_from = scrapy.Field()
    salary_to = scrapy.Field()
    industry_field = scrapy.Field()
    company_labels = scrapy.Field()
    position_advantage = scrapy.Field()
    job_nature = scrapy.Field()
    work_year = scrapy.Field()
    company_size = scrapy.Field()
    company_full_name = scrapy.Field()



class LgCompanyItem(scrapy.Item):
    company_id = scrapy.Field()
    company_name = scrapy.Field()
    has_job_num = scrapy.Field()
    resume_process_rate = scrapy.Field()
    resume_process_time_cost = scrapy.Field()
    resume_process_comment_num = scrapy.Field()
    company_type = scrapy.Field()
    company_process = scrapy.Field()
    company_size = scrapy.Field()
    company_location = scrapy.Field()