# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/11/7 9:35


class XadminPagintor:
    def __init__(self,total_length,amount_per_page=20,display_pages=7,current_page=1):
        self.total_length = total_length
        self.amount_per_page = amount_per_page
        self.display_pages = display_pages
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = self.total_page
            return
        if self.current_page <= 0:
            self.current_page = 1
        elif self.current_page > self.total_page:
            self.current_page = self.total_page

    @property
    def total_page(self):
        a,b = divmod(self.total_length,self.amount_per_page)
        if b > 0:
            return a+1
        return a

    def page_num(self):
        if self.total_page <= self.display_pages:
            return range(1,self.total_page+1)

        interaval,extra = divmod(self.display_pages,2)
        if self.current_page + interaval >= self.total_page:
            return range(self.total_page-self.display_pages + 1,self.total_page +1)
        elif abs(self.current_page - interaval-1) <=0:
            return range(1,self.display_pages+1)
        if extra > 0:
            return range(self.current_page -interaval, self.current_page + interaval)
        return range(self.current_page -interaval, self.current_page + interaval + 1)

    def content_range(self):
        page = self.current_page
        start = (page-1)*self.amount_per_page
        end = page*self.amount_per_page
        return start,end

