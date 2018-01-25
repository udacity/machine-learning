import sys
from collections import OrderedDict
class Visuals:
    # @staticmethod
    # def classificate(df,num_of_classes,min,max,return_type='list'):
    #     total_range = max - min
    #     each_class_range = total_range / num_of_classes
    #     num_of_classes = total_range / each_class_range
    #     # i = 0
    #     classificated ={}
    #     for index, value in df.iteritems():
    #         # if value >= min:
    #         for i in range(num_of_classes):
    #             if i == 0:
    #                 min_r = min
    #                 max_r = each_class_range
    #             else:
    #                 min_r = (each_class_range * i) + 1
    #                 max_r = each_class_range * (i + 1)
    #             key_name = str(min_r) + '-' + str(max_r)
    #             if key_name not in classificated:
    #                 classificated[key_name] = 0
    #             if min_r <= value <= max_r:
    #                 classificated[key_name] += 1
    #     classificated_list = sorted(classificated.items(), key=lambda x: x[0])
    #     if return_type == 'tuples':
    #         print classificated_list
    #         # print type(classificated.keys())
    #         # print sorted(classificated.keys())
    #         #
    #         # print sorted(classificated.values()
    #         # classes = []
    #         # values = []
    #         # for each_class, value in classificated:
    #         #     classes.append(each_class)
    #         #     values.append(value)
    #         # print classes
    #         # print values
    #         # sys.exit()
    #         return tuple(classes),tuple(values)
    #     return classificated_list
    # def classificate(df,num_of_classes,r_min,r_max,return_type='ordered_dict'):
    #     total_range = r_max - r_min
    #     each_class_range = total_range / num_of_classes
    #     classificated = OrderedDict()
    #     if num_of_classes == r_max + 1:
    #         for i in range(0, num_of_classes):
    #             classificated[i]=0
    #     else:
    #         for i in range(0,num_of_classes):
    #             if i == 0:
    #                 classificated[str(r_min) + '-' + str((each_class_range))] = 0
    #             else:
    #                 classificated[str((each_class_range * i) + 1) + '-' + str(each_class_range * (i + 1))] = 0
    #     for index, value in df.iteritems():
    #         num_of_iter = num_of_classes
    #         if num_of_classes == r_max + 1:
    #             num_of_iter += 1
    #         for i in range(num_of_iter):
    #             if num_of_classes == r_max + 1:
    #                 if i == value:
    #                     classificated[i] += 1
    #             else:
    #                 if i == 0:
    #                     each_r_min = r_min
    #                     each_r_max = each_class_range
    #                 else:
    #                     each_r_min = (each_class_range * i) + 1
    #                     each_r_max = each_class_range * (i + 1)
    #                 key_name = str(each_r_min) + '-' + str(each_r_max)
    #                 if each_r_min <= value <= each_r_max:
    #                     classificated[key_name] += 1
    #     if return_type == 'tuples':
    #         return tuple(classificated.keys()),tuple(classificated.values())
    #     return classificated

    def apply_range_classification(self,df,num_of_classes,r_min,r_max,return_type='ordered_dict'):
        total_range = r_max - r_min
        each_class_range = total_range / num_of_classes
        classificated = OrderedDict()
        for i in range(0, num_of_classes):
            if i == 0:
                classificated[str(r_min) + '-' + str((each_class_range))] = 0
            else:
                classificated[str((each_class_range * i) ) + '-' + str(each_class_range * (i + 1))] = 0
        for index, value in df.iteritems():
            for i in range(num_of_classes):
                if i == 0:
                    each_r_min = r_min
                    each_r_max = each_class_range
                else:
                    each_r_min = (each_class_range * i)
                    each_r_max = each_class_range * (i + 1)
                key_name = str(each_r_min) + '-' + str(each_r_max)
                if each_r_min <= value < each_r_max:
                    classificated[key_name] += 1
        if return_type == 'tuples':
            return tuple(classificated.keys()),tuple(classificated.values())
        return classificated

    def apply_simple_classification(self,df,r_min,r_max,return_type='ordered_dict'):
        classificated = OrderedDict()
        for i in range(r_min, r_max + 1):
            classificated[i] = 0
        for index, value in df.iteritems():
            for i in range(r_min,r_max + 1):
                if i == value:
                    classificated[i] += 1
        if return_type == 'tuples':
            return tuple(classificated.keys()),tuple(classificated.values())
        return classificated

    def classificate(self,df,num_of_classes,r_min,r_max,return_type='ordered_dict'):
        if num_of_classes == r_max + 1:
            return self.apply_simple_classification(df,r_min,r_max,return_type)
        else:
            return self.apply_range_classification(df, num_of_classes, r_min, r_max,return_type)

    def display_min_and_max_values(self,df, column, label, separator):
        print label + str(df[column].min()) + separator + str(df[column].max())
# def autolabel(rects):
        #         """
        #         Attach a text label above each bar displaying its height
        #         """
        #         for rect in rects:
        #                 height = rect.get_height()
        #                 # print str(height / len(df) * 100)  + '%'
        #                 # sys.exit()
        #                 ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
        #                         str(height / len(df) * 100) + '%',
        #                         ha='center', va='bottom')
        # autolabel(rects1)
        # autolabel(rects2)
        # autolabel(rects3)