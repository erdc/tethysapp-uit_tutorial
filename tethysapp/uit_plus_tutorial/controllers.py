import os
import datetime as dt
from django.contrib import messages
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
            'data-toggle': 'tooltip',
            'data-placement': 'top',
            'title': 'Submit Job',
            'onclick': 'update_next_button(this);'
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
        max_cleanup_time=dt.timedelta(minutes=5),
        job_script=job_script,
        transfer_input_files=[test_job_in, ],
        transfer_output_files=['test_job.out']
    )
    try:
        job.execute()
    except RuntimeError as e:
        messages.add_message(request, messages.ERROR, 'Failed to Run Job: {}'.format(e))
        job.delete()
        return redirect(reverse('uit_plus_tutorial:home'))

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
        results_url='uit_plus_tutorial:result',
        run_btn=False,
        hover=False,
        striped=True,
        bordered=False,
        condensed=False,
        refresh_interval=5000,
        delete_btn=True,
    )

    context = {
        'jobs_table': jobs_table
    }

    return render(request, 'uit_plus_tutorial/status.html', context)


@ensure_oauth2(app.PROVIDER_NAME)
def result(request, job_id):
    # Using job manager to get the specified job.
    job_manager = app.get_job_manager()
    job = job_manager.get_job(job_id=job_id)

    # Get result and Key
    name = job.name
    results = {}
    for file in job.transfer_output_files:
        path = os.path.join(job._local_transfer_dir, file)
        with open(path) as f:
            results[file] = f.read()

    home_button = Button(
        display_text='Home',
        name='home_button',
        attributes={
            'data-toggle': 'tooltip',
            'data-placement': 'top',
            'title': 'Home'
        },
        href=reverse('uit_plus_tutorial:home')
    )

    jobs_button = Button(
        display_text='Show All Jobs',
        name='jobs_button',
        attributes={
            'data-toggle': 'tooltip',
            'data-placement': 'top',
            'title': 'Show All Jobs'
        },
        href=reverse('uit_plus_tutorial:status')
    )

    context = {'results': results, 'job': job, 'home_button': home_button, 'jobs_button': jobs_button}

    return render(request, 'uit_plus_tutorial/results.html', context)