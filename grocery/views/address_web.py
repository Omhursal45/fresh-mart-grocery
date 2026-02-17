from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Address

@login_required
def address_create_view(request):
    if request.method == 'POST':
        is_default = request.POST.get('is_default') == 'on'

        if is_default:
            Address.objects.filter(user=request.user, is_default=True).update(is_default=False)

        Address.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address_line1=request.POST.get('address_line1'),
            address_line2=request.POST.get('address_line2', ''),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            postal_code=request.POST.get('postal_code'),
            country=request.POST.get('country', 'India'),
            is_default=is_default,
        )

        messages.success(request, 'Address added successfully!')
        return redirect('profile')

    return render(request, 'grocery/address_form.html', {'action': 'Add'})



@login_required
def address_update_view(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        is_default = request.POST.get('is_default') == 'on'

        if is_default:
            Address.objects.filter(user=request.user, is_default=True).exclude(id=address.id).update(is_default=False)

        address.name = request.POST.get('name')
        address.phone = request.POST.get('phone')
        address.address_line1 = request.POST.get('address_line1')
        address.address_line2 = request.POST.get('address_line2', '')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.postal_code = request.POST.get('postal_code')
        address.country = request.POST.get('country', 'India')
        address.is_default = is_default
        address.save()

        messages.success(request, 'Address updated successfully!')
        return redirect('profile')

    return render(request, 'grocery/address_form.html', {'address': address, 'action': 'Edit'})



@login_required
def address_delete_view(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address deleted successfully!')
        return redirect('profile')
    return render(request, 'grocery/address_delete.html', {'address': address})
