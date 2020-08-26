from flask import flash, render_template, current_app
from ..emails import send_email
from ..models import Feedback, db
from .forms import FeedbackForm
from . import feedback_bp


@feedback_bp.route('/', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        author = form.name.data
        body = form.body.data
        message = Feedback(body=body, author=author)
        db.session.add(message)
        db.session.commit()
        recipients = current_app.config['ADMIN_EMAIL_LIST']
        send_email(
            recipients=recipients,
            subject="A new feedback was added!",
            template="feedback/feedback_notification",
            **dict(author=author, content=body)
        )
        flash('Your feedback has been sent to the admins!', "success")
    return render_template('feedback/feedback.html', form=form)
