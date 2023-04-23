from interface.utils.log_utils import loggerr
from django.contrib import auth
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user, assign_perm, remove_perm, get_perms
from interface.config import iWebServerBaseConfig
from interface.models import UserControl

Log = loggerr(__name__).getLogger()


class UserControlUtils:
    def __init__(self):
        self.PermissionNameInfo = {}
        self.PermissionNameInfo['2'] = ['view_idms',
                                           'view_alarms',
                                           'dx_idms',
                                           'view_sidebar',
                                           'edit_live_channel_item',
                                           'view_dashboard_area']

        self.PermissionNameInfo['1'] = ['edit_idms_elk_url',
                                           'remote_assistance',
                                           'edit_business',
                                           'edit_log_config',
                                           'edit_app_config',
                                           'edit_group_config',
                                           'edit_app_blacklist_config',
                                           'edit_app_single_options_config',
                                           'edit_app_batch_options_config',
                                           'edit_dynamic_protecting_config',
                                           'view_businesses',
                                           'view_bi_report',
                                           'view_business_log_list',
                                           'view_business_ratings_list',
                                           'view_business_media_list',
                                           'user_management',
                                           'timed_task',
                                           'device_debug',
                                           'delete_live_channel_item',
                                           'view_live_channel_item',
                                           'device_logger'] + self.PermissionNameInfo['2']

    def GetPermissions(self, Level):
        return self.PermissionNameInfo[str(Level)]

    def GetPermissionObjectByUser(self, user, permission_name):
        try:
            user_controls = get_objects_for_user(user, permission_name, UserControl.objects.all())
            if(user_controls.count() > 1):
                Log.info('WARNING:find more than one permission objects')
            return user_controls.last()
        except Exception as err:
            Log.error('GetPermissionObjectByUser err:[' + str(err) + ']')
        return None

    def GetPermissionObjectByDevice(self, MacAddress=None, SerialNumber=None, deviceName=None):
        # try:
        #     if((MacAddress == None or MacAddress == '') and (SerialNumber == None or SerialNumber == '') and (deviceName == None or deviceName == '')):
        #         return None
        #     devices = Topic.objects.all()
        #     if(MacAddress != None and MacAddress != ''):
        #         devices = devices.filter(MacAddress=MacAddress)
        #     if (SerialNumber != None and SerialNumber != ''):
        #         devices = devices.filter(SerialNumber=SerialNumber)
        #     if (deviceName != None and deviceName != ''):
        #         devices = devices.filter(deviceName=deviceName)
        #     device = devices.last()
        #     if(device == None):
        #         Log.error('GetPermissionObjectByDevice:can not find device')
        #         return None
        #     if(device.area == None):
        #         Log.error('GetPermissionObjectByDevice:can not find area info for ' + device.deviceName)
        #         return UserControl.objects.filter(Level=1).last()
        #     #TODO:
        #     permission_object = UserControl.objects.filter(AreaName=device.area.RegionName, Level=3).last()
        #     if(permission_object == None):
        #         permission_object = UserControl.objects.filter(AreaName=device.area.CityName, Level=2).last()
        #         if(permission_object == None):
        #             permission_object = UserControl.objects.filter(AreaName=device.area.ProvinceName, Level=1).last()
        #     return permission_object
        # except Exception as err:
        #     Log.error('GetPermissionObjectByDevice err:[' + str(err) + ']')
        return None

    def CheckUserDevicePermission(self, request, device, permission_name):
        try:
            if (request.user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))):
                return True
            if(permission_name != None and request.user.has_perm('boards.{}'.format(permission_name))):
                return True
            device_permission_object = self.GetPermissionObjectByDevice(MacAddress=device.MacAddress)
            user_permission_object = self.GetPermissionObjectByUser(request.user, permission_name)
            if(device_permission_object == None or user_permission_object == None):
                return False
            if(device_permission_object == user_permission_object):
                Log.info('CheckUserDevicePermission:check succeed')
                return True
            device_permission_object = device_permission_object.super_control
            while(device_permission_object != None and device_permission_object.Level >= 1):
                if (device_permission_object == user_permission_object):
                    Log.info('CheckUserDevicePermission:check succeed')
                    return True
                device_permission_object = device_permission_object.super_control
        except Exception as err:
            Log.error('CheckUserDevicePermission err:[' + str(err) + ']')
        return False

    def CheckPermissionOnjectByRequest(self, request, permission_name):
        try:
            if (request.user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))):
                return True
            if(permission_name != None and request.user.has_perm('boards.{}'.format(permission_name))):
                return True
            user_permission_object = self.GetPermissionObjectByUser(request.user, permission_name)
            if(user_permission_object != None):
                Log.info('CheckPermissionOnjectByRequest:check succeed')
                return True
        except Exception as err:
            Log.error('CheckPermissionOnjectByRequest err:[' + str(err) + ']')
        Log.error('CheckPermissionOnjectByRequest:check failed')
        return False

    def AssignPermissionToObject(self, PermissionName, AreaName):
        if(PermissionName == None or PermissionName == '' or AreaName == None or AreaName == ''):
            return False
        permission_object = UserControl.objects.filter(AreaName=AreaName).last()
        group = Group.objects.filter(name=AreaName).last()
        if(permission_object == None or group == None):
            Log.error('AssignPermissionToObject:can not assign permission {} for group {}'.format(PermissionName, AreaName))
            return False
        assign_perm(PermissionName, group, permission_object)
        Log.info('AssignPermissionToObject')
        return True

    def GetObjectPermissions(self, AreaName):
        if (AreaName == None or AreaName == ''):
            return None
        permission_object = UserControl.objects.filter(AreaName=AreaName).last()
        group = Group.objects.filter(name=AreaName).last()
        if (permission_object == None or group == None):
            Log.error('GetObjectPermissions:can not get permission for group {}'.format(AreaName))
            return None
        return get_perms(group, permission_object)

    def CheckPermissionToObject(self, PermissionName, AreaName):
        if(PermissionName == None or PermissionName == '' or AreaName == None or AreaName == ''):
            return False
        perms = self.GetObjectPermissions(AreaName)
        return perms != None and PermissionName in perms

    def AssignPermissionToAllObjects(self, PermissionName, Level=None):
        if (PermissionName == None or PermissionName == ''):
            return False
        group_info_list = []
        for permission_object in (UserControl.objects.all() if(Level == None) else UserControl.objects.filter(Level=Level)):
            group = Group.objects.filter(name=permission_object.AreaName).last()
            if (group == None):
                Log.error('AssignPermissionToAllObjects:can not assign permission {} for group {}'.format(PermissionName, permission_object.AreaName))
                return False
            group_info_list.append({'permission_object': permission_object, 'group': group})
        for group_info in group_info_list:
            assign_perm(PermissionName, group_info['group'], group_info['permission_object'])
            Log.error('AssignPermissionToAllObjects:assign permission {} for group {} succeed'.format(PermissionName, group_info['group'].name))
        return True

    def RemovePermissionToAllObjects(self, PermissionName, Level=None):
        if (PermissionName == None or PermissionName == ''):
            return False
        group_info_list = []
        for permission_object in (UserControl.objects.all() if(Level == None) else UserControl.objects.filter(Level=Level)):
            group = Group.objects.filter(name=permission_object.AreaName).last()
            if (group == None):
                Log.error('RemovePermissionToAllObjects:can not remove permission {} for group {}'.format(PermissionName, permission_object.AreaName))
                return False
            group_info_list.append({'permission_object': permission_object, 'group': group})
        for group_info in group_info_list:
            remove_perm(PermissionName, group_info['group'], group_info['permission_object'])
            Log.error('RemovePermissionToAllObjects:remove permission {} for group {} succeed'.format(PermissionName, group_info['group'].name))
        return True

    def InitPermissionObject(self):
        for Level, PermissionNameList in self.PermissionNameInfo.items():
            for PermissionName in PermissionNameList:
                self.AssignPermissionToAllObjects(PermissionName, Level=int(Level))

    def InitUserControlObjects(self, province_name, city_name_list):
        province = UserControl.objects.filter(AreaName=province_name, Level=1).first()
        province = province if (province != None) else UserControl.objects.create(Name=province_name, Desc=province_name, AreaName=province_name, Level=1)
        city_name_list_exist = [item.AreaName for item in UserControl.objects.filter(Level=2, super_control=province)]
        for item in city_name_list:
            if (item in city_name_list_exist):
                continue
            city = UserControl.objects.create(Name=item, Desc=item, AreaName=item, Level=2, super_control=province)
            Log.info('InitUserControlObjects:create object for {} succeed'.format(city.AreaName))


class UserUtils:
    def __init__(self, username, password):
        try:
            self.user = auth.authenticate(username=username, password=password)
            if(self.user == None):
                Log.error('UserUtils:can not find user ' + str(username))
        except Exception as err:
            Log.exception('UserUtils err:[' + str(err) + ']')
            self.user = None

    def get_user(self):
        return self.user

    @staticmethod
    def is_admin(user: User):
        return user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))

    def auto_login(self, request):
        try:
            if(self.user != None):
                auth.login(request, self.user)
                Log.info('login succeed')
                return True
        except Exception as err:
            Log.exception('autologin err:[' + str(err) + ']')
        return False

    def add_user(self, username, password, email, usertype):
        if (self.user == None):
            return False, 'login failed'
        if (not self.user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))):
            return False, 'no permission'
        if (username != None and username != '' and password != None and password != ''):
            try:
                User.objects.create_user(username=username, password=password, email=email)
                return self.set_user_type(username, usertype)
            except Exception as err:
                Log.exception('add_user err:[' + str(err) + ']')
                return False, str(err)

    def delete_user(self, username):
        if (self.user == None):
            return False, 'login failed'
        if (not self.user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))):
            return False, 'no permission'

        try:
            user = get_object_or_404(User, username=username)
            if (user.is_superuser or user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))):
                return False, 'can not delete admin user'
            groups = Group.objects.filter(name='RegularGroup')
            if (groups.count() == 1):
                group = groups[0]
                group.user_set.remove(user)
            user.delete()
            return True, 'succeed'
        except Exception as err:
            Log.exception('delete_user err:[' + str(err) + ']')
            return False, str(err)

    def set_user_type(self, username, usertype):
        if (self.user == None):
            return False, 'login failed'
        if (not self.user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))):
            return False, 'no permission'

        try:
            user = get_object_or_404(User, username=username)
            if (usertype == None):
                return False, 'usertype err'

            if (usertype == 'Regular' and not user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_REGULAR_ACCESS))):
                groups = Group.objects.filter(name='RegularGroup')
                if (len(groups) == 1):
                    group = groups[0]
                    group.user_set.add(user)
                    return True, 'succeed'
            elif (usertype == 'Guest' and user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_REGULAR_ACCESS))):
                groups = Group.objects.filter(name='RegularGroup')
                if (len(groups) == 1):
                    group = groups[0]
                    group.user_set.remove(user)
                    return True, 'succeed'
            return False, 'set usertype to ' + usertype + ' failed'
        except Exception as err:
            Log.exception('set_user_type err:[' + str(err) + ']')
            return False, str(err)