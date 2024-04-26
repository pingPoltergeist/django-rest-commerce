from .permissions import StaffOfTheOrganization
from .models import Permission


class OrderViewPermission(StaffOfTheOrganization):
    message = "Do not have view permission!"

    def has_permission(self, request, view):
        if self.is_organization_owner(request) or self.is_organization_owner(request):
            return True
        staff_of_org: Permission = self.check_and_get_staff_of_the_organization(request)
        if not staff_of_org:
            return False
        return staff_of_org.have_product_view_permission()


class OrderExecutePermission(StaffOfTheOrganization):
    message = "Do not have edit permission on product!"

    def has_permission(self, request, view):
        if self.is_organization_owner(request) or self.is_organization_owner(request):
            return True
        staff_of_org: Permission = self.check_and_get_staff_of_the_organization(request)
        if not staff_of_org:
            return False
        return staff_of_org.have_product_view_edit_permission()


class OrderExecuteOrRejectPermission(StaffOfTheOrganization):
    message = "Do not have all permission on product!"

    def has_permission(self, request, view):
        if self.is_organization_owner(request) or self.is_organization_owner(request):
            return True
        staff_of_org: Permission = self.check_and_get_staff_of_the_organization(request)
        if not staff_of_org:
            return False
        return staff_of_org.have_all_product_permission()
