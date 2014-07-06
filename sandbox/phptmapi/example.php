<?php
# Path to your PHPTMAPI 2.0 lib
require_once('quaaxtm/lib/phptmapi2.0/core/TopicMapSystemFactory.class.php');

$tmSysFactory = TopicMapSystemFactory::newInstance();

$tmSys = $tmSysFactory->newTopicMapSystem();

$tm = $tmSys->getTopicMap('http://www.example.org/map');

# Populate the topic map only iff it does not exist already. :)
if (is_null($tm)) {
  # Importing the tm may take some time.
  ini_set('max_execution_time', '300');
  $tm = $tmSys->createTopicMap('http://www.example.org/map');
  include('pokemon.ltm.php');
  populate_map($tm);
}

echo count($tm->getTopics());
?>