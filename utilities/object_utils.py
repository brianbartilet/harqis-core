import re


class ObjectUtil:

    @staticmethod
    def obj_to_sc(cur_object=None):
        '''
         convert dict keys into snake_case
        '''
        object_type = type(cur_object)
        obj_dict = cur_object.__dict__
        for key, value in obj_dict.copy().items():
            snake_case_key = ObjectUtil.convert_to_sc(key)
            if snake_case_key != key:
                obj_dict[snake_case_key] = obj_dict[key]
                del obj_dict[key]
        new_obj = object_type(**obj_dict)
        return new_obj

    @staticmethod
    def obj_list_to_sc(object_collection=None):
        '''
         convert list of objects dict keys into snake_case
        '''
        new_list = []
        for item in object_collection:
            new_obj = ObjectUtil.obj_to_sc(item)
            new_list.append(new_obj)

        return new_list

    @staticmethod
    def convert_obj_to_sc(object_item=None):
        '''
         convert list of objects dict keys into snake_case
        '''
        #  pass thru if failed
        try:
            if isinstance(object_item, list) or isinstance(object_item, dict):
                return ObjectUtil.obj_list_to_sc(object_item)
            else:
                return ObjectUtil.obj_to_sc(object_item)
        except:
            return object_item



    @staticmethod
    def obj_list_to_specific_obj_list(object_collection=None, object_type=None):
        '''
        Convert list of objects to new object type
        '''
        new_list = []
        for item in object_collection:
            new_obj = object_type(**item.__dict__)
            new_list.append(new_obj)
        return new_list

    @staticmethod
    def convert_to_sc(text):
        '''
        Convert text to snake case
        This should support pascal and camel case
        '''
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', text)
        return '_'.join(map(str.lower, words))
