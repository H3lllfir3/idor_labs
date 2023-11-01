### Vulnerable code

    ```python
    def profile(request, acc_id):
        user = Profile.objects.get(acc=acc_id)
        ...
    ```

### Safe code
    - we should alwayse check the user id from the session and compre it 
    with requested data to prevent IDOR and other type of vulnerbility.

    ```python
    def profile(request, acc_id):
        user = Profile.objects.get(acc=acc_id)
        if request.user.id == user.id:
            # ALLOW ACTION
            # VALIDATE REQUEST DATA
            form = AccountForm(instance=user, request=request)
            ...
        else:
            # DENY ACTION
    ```