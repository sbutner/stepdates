import os
import time
import pandas as pd

class Customer(object):
    def __init__(self, gp_id, customer_name, review_path):
        self.gp_id = gp_id
        self.customer_name = customer_name
        self.review_path = review_path
        self.log = self.make_table()

    @staticmethod
    def parse_date(folder):
        month, day, year, time = (folder[8:10], folder[11:13], folder[14:18],folder[20:])
        if len(time) > 4:
            if (int(time) < 600):
                        day = int(day) - 1
        date_string = month+'/'+str(day)+'/'+year
        return date_string
    @staticmethod
    def is_review_sheet(path, stage):
        if stage == "First":
            return '.xls' in path and ' - Final' not in path
        elif stage == "Third":
            return '.xls' in path and ' - Final Invoice Review' in path        
        elif stage == "Fourth":
            return '.xls' in path and ' - Final' in path
    @staticmethod
    def get_time(path, mode="c"):
        if (mode == "c" or mode == "created"):
            date = time.gmtime(os.path.getctime(path))
            if (date[3] < 7):
                day = date[2] - 1
            else:
                day = date[2]
            date_string = str(date[1])+'/'+str(day)+'/'+str(date[0])
            return date_string
        elif (mode == "m" or mode == "modified"):
            date = parse_date(path)
            return date
    @staticmethod
    def _walk_through_customer(directory):
        logging.debug('Checking if directory is fourth stage: {}'.format(directory))
        if (os.path.split(directory)[1].lower() == 'ireview'):
            logging.debug('{} is fourth stage'.format(directory))
            paths = []
            for pt, dn, fn in os.walk(directory):
                logging.debug('Checking if {} is timestamped iReview folder'.format(pt))
                if len(os.path.split(pt)[1]) > 5:
                    logging.debug('{} is timestamped iReview folder'.format(pt))
                    paths.append(pt)
                logging.debug('{} is not timestamped iReview folder'.format(pt))
            return paths
        else:
            logging.debug('{} is not fourth stage'.format(directory))
            paths = []
            for pt, dn, fn in os.walk(directory):
                for fi in fn:
                    paths.append(pt+'\\'+fi)
            return paths



    def make_table(self):
        customer_tree = _compile_customer()
        customer_tree = _unroll_customer(customer_tree)
        out = []
        for key, val in enumerate(unrolledCustomer):
            _ = [customerName, val]
            for i in ['first_stage', 'third_stage', 'fourth_stage']:
                try:
                    _.append(unrolledCustomer[val][i])
                except KeyError:
                    _.append('NA')
            out.append(_)
    def _compile_customer(self):
        customerResults = dict({'customer_name' : self.customer_name,
                                        'first_stage' : _get_first_stage(),
                                        'third_stage' : _get_third_stage(),
                                        'fourth_stage' : _get_fourth_stage()})
        return customer_dates

    def _unroll_customer(self, customer_dict):
        unroll = {}
        for key, val in enumerate(customer_dict):
            if val != 'customer_name':
                for k, v in enumerate(customer_dict[val]):
                    unroll[v[0]] = {}
                    unroll[v[0]][val] = v[1]
        return unroll
    
    def _get_first_stage(self):
        path = self.path+'prior months'
        files = _walk_through_customer(path)
        dates = {(os.path.split(file)[1][0:5],get_time(file, mode="c")) for file in files}
        return dates

    def _get_third_stage(self):
        path = self.path+'Final Invoice Review'
        files = _walk_through_customer(path)
        dates = {(os.path.split(file)[1][0:5],get_time(file, mode="c")) for file in files if is_review_sheet(file, "Third")}
        return dates    

    def _get_fourth_stage(self):
        path = self.path+'ireview'
        folders = _walk_through_customer(path)
        dates = {(folder[0:5],parseDate(folder)) for folder in folders if os.path.isdir(folder)}
        return dates

def validate_folder(path):
    if os.path.isdir(path):
        return (secret.VALID_SUBFOLDER in os.listdir(path))



if __name__ == "__main__":
