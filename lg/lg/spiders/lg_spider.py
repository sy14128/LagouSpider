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
        self.company_ids = set()
        pass

    def __del__(self):
        pass

    def make_form_request(self,first,job,page_no,callback):
        formdata = {'first':first,'kd':job,'pn':page_no}
        return FormRequest(url="http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false",method="post",formdata=formdata,callback=callback,meta=formdata)
    
    
    def start_requests(self):
        requests = []
        for job in jobs:
            requests.append(
                make_form_request(job,'1',self.parse)
            )
        return requests
    
    def parse(self, response):
        res = json.loads(response.body)
        page_no = int(res['content']['pageNo'])
        page_size = int(res['content']['pageSize'])
        total_count = int(res['content']['totalCount'])
        for job in res['result']:
            if job['positionId'].isdigit() == False:
                continue
            business_zones = ','.join(job['businessZones'])
            salary_full = job['salary'].split('|')
            salary_from = salary_full[0][:-1]
            salary_to = salary_to[1][:-1]
            company_labels = ','.join(job['companyLabelList'])
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
                company_url = 'http://www.lagou.com/gongsi/' + job['companyId'] + '.html'
                yield scrapy.Request(company_url, callback=self.company_parse ,meta={'company_id':job['companyId']})
        #最后处理下一页
        if page_no < ((total_count / page_size) + 1):
            yield make_form_request('false',response.meta['job'],page_no + 1,self.parse)
        
        self.job_list_file.write(response.body)

    def company_parse(self,response):
        selector = Selector(text=response.body)
        company_item = CompanyItem({
            'company_id': response.meta['company_id'],
            'company_name': selector.xpath('/html/body/div[2]/div/div/div[1]/h1/a/text()').extract().strip(),
            'has_job_num' : selector.xpath('/html/body/div[2]/div/div/div[2]/ul/li[1]/strong/text()').extract().strip(),
            'resume_process_rate' : selector.xpath('/html/body/div[2]/div/div/div[2]/ul/li[2]/strong/text()').extract().strip(),
            'resume_process_time_cost' : selector.xpath('/html/body/div[2]/div/div/div[2]/ul/li[3]/strong/text()').extract().strip(),
            'resume_process_comment_num' : selector.xpath('//*[@id="mspj"]/strong/text()').extract().strip(),
            'company_type' : selector.xpath('//*[@id="basic_container"]/div[2]/ul/li[1]/span/text()').extract().strip(),
            'company_process' : selector.xpath('//*[@id="basic_container"]/div[2]/ul/li[2]/span/text()').extract().strip(),
            'company_size' : selector.xpath('//*[@id="basic_container"]/div[2]/ul/li[3]/span/text()').extract().strip(),
            'company_location' : selector.xpath('//*[@id="basic_container"]/div[2]/ul/li[4]/span/text()').extract().strip(),
        })
        yield company_item