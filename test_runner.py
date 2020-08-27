from unittest import TestCase
import pytest
import subprocess

def test_should_run_cmd_n_times_succefully_and_collect_its_output(fake_process):
    
    fake_process.keep_last_process(True)
    
    # any command can be called
    fake_process.register_subprocess([fake_process.any()])

    subprocess.check_call(["ping", "-c 2", "google.com"])
    subprocess.check_call(["ping", "-h"])
    # subprocess.check_call(["ping", "/source", "/other/destination"])

    # you can check if command is in ``fake_process.calls``
    assert ["ping", "-c 2", "google.com"] in fake_process.calls
    assert ["ping", "-h"] in fake_process.calls
    # assert ["cp", "/source", "/other/destination"] in fake_process.calls

    # or check how many it was called, possibly with wildcard arguments
    assert fake_process.call_count(["ping", "-c 2", "google.com"]) == 1

    # with ``call_count()`` you don't need to use the same type as
    # the subprocess was called
    assert fake_process.call_count("ping -h") == 1

   
          
                           

