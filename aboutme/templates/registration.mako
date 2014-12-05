<%inherit file="base.mako"/>
<%block name="title">Регистрация на сайте</%block>
<%block name="content">

<form action="${request.route_url('registration')}" method="post">
% for error in form.first_name.errors:
    <div class="error">${error}</div>
% endfor
<div>
    <label>${form.first_name.label}</label><br>
    ${form.first_name(maxlength=32)}
</div>

% for error in form.last_name.errors:
    <div class="error">${error}</div>
% endfor
<div>
    <label>${form.last_name.label}</label><br>
    ${form.last_name(maxlength=32)}
</div>

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

<div><input type="submit" value="Зарегистрироваться"></div>
</form>

</%block>