OVERVIEW_ITEMS = ('pay_scale_&_grade',
                'telework_eligible',
                'travel_required',
                'relocation_expenses_reimbursed',
                'appointment_type',
                'work_schedule',
                'service',
                'promotion_potential',
                'job_family_(series)',
                'supervisory_status',
                'security_clearance',
                'drug_test',
                'position_sensitivity_and_risk',
                'trust_determination_process')



class Value_Counter:

    def __init__(self, key_list):
        self.__item_counter__ = {}
        for key in key_list:
            self.__item_counter__.update({key : []})

    def add_card(self, card):
        for key, value in card.items():
            if key in OVERVIEW_ITEMS:
                if value not in self.__item_counter__[key]:
                    self.__item_counter__[key].append(value)

    def store_values(self,filename, no_records):

        with open(filename, 'a') as file:
            file.write("\n\n\nTotally " + str(no_records) + "records analysed\n")
            for key, value in self.__item_counter__.items():
                file.write("\n" + key + "  Take " + str(len(value)) + " values :  " + str(value))

