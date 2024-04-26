from .permissions import StaffOfTheOrganization
from .models import Permission


class OrderViewPermission(StaffOfTheOrganization):
    message = "Do not have view permission for order!"

    def has_permission(self, request, view):
        if self.is_organization_owner(request) or self.is_organization_owner(request):
            return True
        staff_of_org: Permission = self.check_and_get_staff_of_the_organization(request)
        if not staff_of_org:
            return False
        return staff_of_org.have_order_view_permission()


class OrderExecutePermission(StaffOfTheOrganization):
    message = "Do not have execute permission for order!"

    def has_permission(self, request, view):
        if self.is_organization_owner(request) or self.is_organization_owner(request):
            return True
        staff_of_org: Permission = self.check_and_get_staff_of_the_organization(request)
        if not staff_of_org:
            return False
        return staff_of_org.have_order_execute_permission()


class OrderExecuteOrRejectPermission(StaffOfTheOrganization):
    message = "Do not have execute or reject permission for order!"

    def has_permission(self, request, view):
        if self.is_organization_owner(request) or self.is_organization_owner(request):
            return True
        staff_of_org: Permission = self.check_and_get_staff_of_the_organization(request)
        if not staff_of_org:
            return False
        return staff_of_org.have_order_execute_or_reject_permission()
