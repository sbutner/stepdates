import os
import time
import pandas as pd


class Customer(object):
    def __init__(self, gp_id, customer_name, review_path):
        self.gp_id = gp_id
        self.customer_name = customer_name
        self.review_path = review_path

    def init_review_history(self):
        self.log = self.make_table()
        
    @staticmethod
    def is_review_sheet(path, stage):
        if stage.lower() == "first":
            return '.xls' in path and ' - Final' not in path
        elif stage.lower() == "third":
            return '.xls' in path and ' - Final Invoice Review' in path        
        elif stage.lower() == "fourth":
            return '.xls' in path and ' - Final' in path


    @staticmethod
    def parse_date(folder):
        '''extracts the time and date from iReview folders generated on fourth
        step run. Assumes 'YY-MM - dd.mm.yyyy hhmmss' name format'''
        folder = os.path.split(folder)[1]
        month, day, year, time = (folder[8:10], folder[11:13], folder[14:18],folder[20:])
        if len(time) > 4:
            if (int(time) < 600):
                        day = int(day) - 1
        date_string = month+'/'+str(day)+'/'+year
        return date_string
    
    @classmethod
    def _walk_through_customer(cls, directory):
        '''Wrapper for os.walk to handle the expected structures and return a
        flat list of paths to feed into date extraction functions'''
        if (os.path.split(directory)[1].lower() == 'ireview'):
            paths = []
            for pt, dn, fn in os.walk(directory):
                if len(os.path.split(pt)[1]) > 5 and cls._check_folder(pt):    
                    paths.append(pt)
            return paths
        else:
            paths = []
            for pt, dn, fn in os.walk(directory):
                for fi in fn:
                    paths.append(pt+'\\'+fi)
            return paths

    @staticmethod
    def _check_folder(folder):
        try:
            int(os.path.split(folder)[1][0:1])
            return True
        except ValueError:
            return False
            

    def make_table(self):
        customer_tree = self._compile_customer()
        customer_tree = self._unroll_customer(customer_tree)
        out = []
        for key, val in enumerate(customer_tree):
            try:
                int(val[0])
                _ = [self.customer_name, val]
                for i in ['first_stage', 'third_stage', 'fourth_stage']:
                    try:
                        _.append(customer_tree[val][i])
                    except KeyError:
                        _.append('NA')
                out.append(_)
            except ValueError:
                pass
        return out
    
    def _compile_customer(self):
        customer_dates = dict({'customer_name' : self.customer_name,
                                        'first_stage' : self._get_first_stage(),
                                        'third_stage' : self._get_third_stage(),
                                        'fourth_stage' : self._get_fourth_stage()})
        return customer_dates

    def _unroll_customer(self, customer_dict):
        unroll = {}
        for key, val in enumerate(customer_dict):
            if val != 'customer_name':
                for k, v in enumerate(customer_dict[val]):
                    try:
                        unroll[v[0]][val] = v[1]
                    except KeyError:
                        unroll[v[0]] = {}
                        unroll[v[0]][val] = v[1]
        return unroll
    
    def _get_first_stage(self):
        path = self.review_path+'prior months'
        files = self._walk_through_customer(path)
        dates = {(os.path.split(file)[1][0:5], self._get_time(file, mode="c")) for file in files if self.is_review_sheet(file, "First")}
        return dates

    def _get_third_stage(self):
        path = self.review_path+'Final Invoice Review'
        files = self._walk_through_customer(path)
        dates = {(os.path.split(file)[1][0:5], self._get_time(file, mode="c")) for file in files if self.is_review_sheet(file, "Third")}
        return dates    

    def _get_fourth_stage(self):
        path = self.review_path+'ireview'
        folders = self._walk_through_customer(path)
        dates = {(os.path.split(folder)[1][0:5], self._get_time(folder, mode="m")) for folder in folders if os.path.isdir(folder)}
        return dates

    def _get_time(self, path, mode="c"):
        if (mode == "c" or mode == "created"):
            date = time.gmtime(os.path.getctime(path))
            if (date[3] < 7):
                day = date[2] - 1
            else:
                day = date[2]
            date_string = str(date[1])+'/'+str(day)+'/'+str(date[0])
            return date_string
        elif (mode == "m" or mode == "modified"):
            date = self.parse_date(path)
            return date

def main():
    pass

if __name__ == "__main__":
    main()
