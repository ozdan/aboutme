<%inherit file="base.mako"/>
<%block name="title">Регистрация на сайте</%block>
<%block name="content">

<div>
    <form action="${request.route_url('login')}" method="post">
        <div class="error">${message}</div>
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

        <div><input type="submit" value="Войти"></div>
    </form>
</div>

</%block>