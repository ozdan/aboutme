<%inherit file="base.mako"/>
<%block name="title">Регистрация на сайте</%block>
<%block name="content">

<form action="${request.route_url('user_edit', username=request.authenticated_userid)}" method="post" enctype="multipart/form-data">

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

% for error in form.biography.errors:
    <div class="error">${error}</div>
% endfor
<div>
    <label>${form.biography.label}</label><br>
    ${form.biography(cols=35, rows=5)}
</div>

% for error in form.location.errors:
    <div class="error">${error}</div>
% endfor
<div>
    <label>${form.location.label}</label><br>
    ${form.location(maxlength=50)}
</div>

% for error in form.work.errors:
    <div class="error">${error}</div>
% endfor
<div>
    <label>${form.work.label}</label><br>
    ${form.work(maxlength=50)}
</div>

% for error in form.education.errors:
    <div class="error">${error}</div>
% endfor
<div>
    <label>${form.education.label}</label><br>
    ${form.education(maxlength=70)}
</div>

% for error in form.interest.errors:
    <div class="error">${error}</div>
% endfor
<div>
    <label>${form.interest.label}</label><br>
    ${form.interest(maxlength=30)}
</div>

% for error in form.picture.errors:
    <div class="error">${error}</div>
% endfor
<div>
    <label>${form.picture.label}</label><br>
    ${form.picture()}
</div>

<div><input type="submit" value="Сохранить изменения"></div>
</form>

</%block>