<%inherit file="base.mako"/>
<%block name="title">Регистрация на сайте</%block>
<%block name="content">

<form action="${request.route_url('account')}" method="post">

% for error in form.email.errors:
    <div class="error">${error}</div>
% endfor
<div>
    <label>${form.email.label}</label><br>
    ${form.email(maxlength=64)}
</div>

% for error in form.username.errors:
    <div class="error">${error}</div>
% endfor
<div>
    <label>${form.username.label}</label><br>
    ${form.username(maxlength=32)}
</div>

% for error in form.password.errors:
    <div class="error">${error}</div>
% endfor
<div>
    <label>${form.password.label}</label><br>
    ${form.password()}
</div>

<div><input type="submit" value="Сохранить изменения"></div>
</form>

</%block>