from rest_framework.permissions import BasePermission
from ORGANIZATION.models import Organization, Permission


class StaffOfTheOrganization(BasePermission):
    message = 'Access Denied!'

    def check_and_get_organization(self, request):
        org_path = '/org/'
        path = request.META.get('PATH_INFO')
        org_id = path[path.find(org_path) + org_path.__len__():].split('/')[0]
        org_qs = Organization.objects.filter(id=org_id)
        return org_qs.first() if org_qs.count() == 1 else None

    def is_organization_owner(self, request):
        org: Organization = self.check_and_get_organization(request)
        return bool(org.owner == request.user.username) if org else False

    def is_organization_admin(self, request):
        org: Organization = self.check_and_get_organization(request)
        if org:
            permission: Permission = request.user.username.permission_set.get(organization=org)
            return bool(permission.role == Permission.ROLE.ADMIN)
        else:
            return False

    def is_staff_of_the_organization(self, request):
        if self.is_organization_admin(request) or self.is_organization_owner(request):
            return True
        org: Organization = self.check_and_get_organization(request)
        return bool(org.staff.filter(staff=request.user.username)) if org else False

    def has_permission(self, request, view):
        return self.is_staff_of_the_organization(request)


class OrganizationOwnerOnly(StaffOfTheOrganization):
    message = "Only Owner can perform this action!"

    def has_permission(self, request, view):
        return self.is_organization_owner(request)


class OrganizationAdminOnly(StaffOfTheOrganization):
    message = "Only Admin can perform this action!"

    def has_permission(self, request, view):
        if self.is_organization_owner(request):
            return True
        if not self.is_staff_of_the_organization(request):
            return False
        return self.is_organization_admin(request)
