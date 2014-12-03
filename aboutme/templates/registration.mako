<%inherit file="base.mako"/>
<%block name="title">Регистрация на сайте</%block>
<%block name="content">

<form action="${request.route_url('login')}" method="post">
% for error in form.first_name.errors:
    <div class="error">${error}</div>
% endfor
<div><label>${form.first_name.label}</label>${form.first_name()}</div>

% for error in form.last_name.errors:
    <div class="error">${error}</div>
% endfor
<div><label>${form.last_name.label}</label>${form.last_name()}</div>

% for error in form.email.errors:
    <div class="error">${error}</div>
% endfor
<div><label>${form.email.label}</label>${form.email()}</div>

<div><input type="submit" value="Submit"></div>
</form>

</%block>