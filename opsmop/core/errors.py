# Copyright 2018 Michael DeHaan LLC, <michael@michaeldehaan.net>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class OpsMopError(Exception):

    """
    The basis for all types of OpsMop Errors, this one really should not be used directly.
    """

    __slots__ = [ 'msg' ]

    def __init__(self, msg):
        self.msg = msg

class OpsMopStop(Exception):
    pass

class ValidationError(OpsMopError):

    """
    This is the type of error that gets called when a resource has invalid arguments.
    """

    __slots__ = [ 'resource', 'msg' ]
    
    def __init__(self, resource=None, msg=None):
        self.resource = resource
        self.msg = msg

    def __str__(self):
        return "<ValidationError: %s>" % self.msg

class InventoryError(ValidationError):
    pass

class NoSuchProviderError(OpsMopError):
    
    __slots__ = [ 'resource', 'msg' ]

    def __init__(self, resource, provider_name):
        self.resource = resource
        self.msg = "No such provider: %s" % provider_name

    def __str__(self):
        return "<%s>" % self.msg

class ProviderError(OpsMopError):

    """
    This error *may* be raised by a provider for certain internal issues, but in general
    provider apply methods should return self.error('msg') when available.

    This could be used to raise an error in the plan() stage.
    """

    __slots__ = [ 'provider', 'resource', 'msg' ]

    def __init__(self, provider=None, msg=None):
        assert provider is not None
        self.provider = provider
        self.resource = provider.resource
        self.msg = msg

    def __str__(self):
        return "<ProviderError (%s)>" % (self.msg)

class FailedResult(ProviderError):

    __slots__ = [ 'provider', 'resource', 'msg', 'result' ]

    def __init__(self, provider=None, msg=None, result=None):
        assert provider is not None
        self.provider = provider
        self.resource = provider.resource
        self.msg = msg
        self.result = result

    def __str__(self):
        return "<FailedResult (%s)>" % (self.result)
