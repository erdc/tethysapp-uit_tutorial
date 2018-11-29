import os
import datetime as dt
from django.shortcuts import render, redirect, reverse
from tethys_sdk.gizmos import Button, JobsTable
from tethys_sdk.services import ensure_oauth2
from uit_plus_job.models import UitPlusJob
from tethysapp.uit_plus_tutorial.app import UitPlusTutorial as app


@ensure_oauth2(app.PROVIDER_NAME)
def home(request):
    """
    Controller for the app home page.
    """
    next_button = Button(
        display_text='Submit Job',
        name='next-button',
        href=reverse('uit_plus_tutorial:run_job'),
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Submit Job'
        }
    )

    context = {
        'next_button': next_button
    }

    return render(request, 'uit_plus_tutorial/home.html', context)

@ensure_oauth2(app.PROVIDER_NAME)
def run_job(request):
    """
    Controller that creates and submits a UIT job.
    """
    # Get Token from Social Auth
    social = request.user.social_auth.get(provider=app.PROVIDER_NAME)
    token = social.extra_data['access_token']

    # Get Needed App Settings
    project_id = app.get_custom_setting('project_id')

    # Get Paths to Files
    app_workspace = app.get_app_workspace()
    test_job_in = os.path.join(app_workspace.path, 'test_job.in')

    uit_plus_tutorial_dir = os.path.dirname(__file__)
    job_script = os.path.join(uit_plus_tutorial_dir, 'job_scripts', 'job_script.py')

    # Get Job Manager
    job_manager = app.get_job_manager()

    job = job_manager.create_job(
        name='TestUitJob',
        user=request.user,
        job_type=UitPlusJob,
        project_id=project_id,
        system='topaz',
        node_type='compute',
        num_nodes=1,
        processes_per_node=1,
        queue='debug',
        max_time=dt.timedelta(minutes=5),
        job_script=job_script,
        transfer_input_files=[test_job_in,],
        transfer_output_files=['test_job.out']
    )

    # client = job.get_client(token=token)
    job._execute(token)

    import pdb; pdb.set_trace()
    return redirect(reverse('uit_plus_tutorial:status'))


@ensure_oauth2(app.PROVIDER_NAME)
def status(request):
    """
    Show Status of Running Jobs on Jobs Table.
    """
    # Get Jobs
    job_manager = app.get_job_manager()
    jobs = job_manager.list_jobs(order_by='-id', filters=None)

    jobs_table = JobsTable(
        jobs=jobs,
        column_fields=('id', 'name', 'description', 'creation_time'),
        hover=True,
        striped=False,
        bordered=False,
        condensed=False,
        refresh_interval=1000,
        delete_btn=True,
    )

    context = {
        'jobs_table': jobs_table
    }

    return render(request, 'uit_plus_tutorial/status.html', context)
