#coding=utf-8
import json
import scrapy
from scrapy import FormRequest
from target_jobs import jobs
from lg.items import LgJobItem as JobItem
from lg.items import LgCompanyItem as CompanyItem

class LgSpider(scrapy.Spider):
    name = "lg"
    allowed_domains = ["lagou.com"]

    def __init__(self):
        self.debug_log = open("debug_log.txt","w")
        self.company_ids = set()

    def __del__(self):
        self.debug_log.close()

    def make_form_request(self,first,job,page_no,callback):
        formdata = {'first':first,'kd':job,'pn':page_no}
        return FormRequest(url="http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false",method="post",formdata=formdata,callback=callback,meta=formdata)
    
    
    def start_requests(self):
        requests = []
        for job in jobs:
            requests.append(
                self.make_form_request("true",job,'1',self.parse)
            )
        return requests
    
    def parse(self, response):
        res = json.loads(response.body)
        page_no = int(res['content']['pageNo'])
        page_size = int(res['content']['pageSize'])
        total_count = int(res['content']['positionResult']['totalCount'])
        for job in res['content']['positionResult']['result']:
            if(type(job['businessZones'])==list):
                business_zones = ','.join(job['businessZones'])
            else:
                business_zones = job['businessZones']
            salary_full = job['salary'].split('-')
            salary_from = salary_full[0][:-1]
            if len(salary_full) == 2:
                salary_to = salary_full[1][:-1]
            else:
                salary_to = salary_from
            if(type(job['companyLabelList'])==list):
                company_labels = ','.join(job['companyLabelList'])
            else:
                company_labels = job['companyLabelList']
            job_item = JobItem({
                'format_create_time':job['formatCreateTime'],
                'publisher_id':job['publisherId'],
                'business_zones':business_zones,
                'create_time':job['createTime'],
                'company_id':job['companyId'],
                'position_name':job['positionName'],
                'education':job['education'],
                'city':job['city'],
                'position_id':job['positionId'],
                'finance_stage':job['financeStage'],
                'company_short_name':job['companyShortName'],
                'company_logo':job['companyLogo'],
                'salary':job['salary'],
                'salary_from':salary_from,
                'salary_to':salary_to,
                'industry_field':job['industryField'],
                'company_labels':company_labels,
                'position_advantage':job['positionAdvantage'],
                'job_nature':job['jobNature'],
                'work_year':job['workYear'],
                'company_size':job['companySize'],
                'company_full_name':job['companyFullName']
            })
            yield job_item
            if job['companyId'] not in self.company_ids:
                self.company_ids.add(job['companyId'])
                company_url = 'http://www.lagou.com/gongsi/' + str(job['companyId']) + '.html'
                yield scrapy.Request(company_url, callback=self.company_parse ,meta={'company_id':job['companyId']})
        limit = ((total_count / page_size) + 1)
        #for test
        limit = 5
        #for next page
        page_no = int(response.meta['pn'])
        if page_no < limit:
            next_request = self.make_form_request('false',response.meta['kd'],str(page_no + 1),self.parse)
            yield next_request
    

    def company_parse(self,response):
        selector = scrapy.Selector(text=response.body)
        company_item = CompanyItem({
            'company_id': response.meta['company_id'],
            'company_name': selector.xpath('/html/body/div[2]/div/div/div[1]/h1/a/text()').extract()[0].strip(),
            'has_job_num' : selector.xpath('/html/body/div[2]/div/div/div[2]/ul/li[1]/strong/text()').extract()[0].strip(),
            'resume_process_rate' : selector.xpath('/html/body/div[2]/div/div/div[2]/ul/li[2]/strong/text()').extract()[0].strip(),
            'resume_process_time_cost' : selector.xpath('/html/body/div[2]/div/div/div[2]/ul/li[3]/strong/text()').extract()[0].strip(),
            'resume_process_comment_num' : selector.xpath('//*[@id="mspj"]/strong/text()').extract()[0].strip(),
            'company_type' : selector.xpath('//*[@id="basic_container"]/div[2]/ul/li[1]/span/text()').extract()[0].strip(),
            'company_process' : selector.xpath('//*[@id="basic_container"]/div[2]/ul/li[2]/span/text()').extract()[0].strip(),
            'company_size' : selector.xpath('//*[@id="basic_container"]/div[2]/ul/li[3]/span/text()').extract()[0].strip(),
            'company_location' : selector.xpath('//*[@id="basic_container"]/div[2]/ul/li[4]/span/text()').extract()[0].strip(),
        })
        yield company_item