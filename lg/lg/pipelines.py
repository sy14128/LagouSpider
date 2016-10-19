# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.exceptions import DropItem
from items import LgJobItem as JobItem
from items import LgCompanyItem as CompanyItem


class LgWritePipeline(object):
    def __init__(self):
        self.position_ids = set()
        self.company_ids = set()
        self.job_file = open("job_file.csv","w")
        self.company_file = open("company_file.csv","w")
        
    def __del__(self):
        self.job_file.close()
        self.company_file.close()
    
    def dic2csv(self,item,out_file):
        count = 0
        for k in item.keys():
            count = count + 1
            out_file.write(str(item[k]))
            if count != len(item):
                out_file.write('\t')
        out_file.write('\n')
    
    def process_item(self, item, spider):
        if isinstance(item, JobItem):
            return self.process_job_item(item,spider)
        elif isinstance(item, CompanyItem):
            return self.process_company_item(item,spider)
        return item
    
    def process_job_item(self,item,spider):
        if item['position_id'] in self.position_ids:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.position_ids.add(item['position_id'])
            self.dic2csv(item,self.job_file)
        return item

    def process_company_item(self,item,spider):
        if item['company_id'] in self.company_ids:
            return item
        else:
            self.company_ids.add(item['company_id'])
            self.dic2csv(item,self.company_file)
        return item
        