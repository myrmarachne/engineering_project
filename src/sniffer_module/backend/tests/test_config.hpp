#include <cppunit/TestFixture.h>
#include <cppunit/TestAssert.h>
#include <cppunit/TestCaller.h>
#include <cppunit/TestSuite.h>
#include <cppunit/TestCase.h>

#include "../config.hpp"

using namespace std;

class TestConfig : public CppUnit::TestFixture {

private:
  Config * testConfig;

public:
  TestConfig() : testConfig(NULL) {
    testConfig = new Config();
  }
	virtual ~TestConfig() {
		delete testConfig;
	}

  static CppUnit::Test *suite() {
  		CppUnit::TestSuite *suiteOfTests = new CppUnit::TestSuite("TestConfig");

  		suiteOfTests->addTest(new CppUnit::TestCaller<TestConfig>("Test parsing a correct config JSON (loading config)",
  				&TestConfig::test_load_config ));

  		suiteOfTests->addTest(new CppUnit::TestCaller<TestConfig>("Test the db_connector_config function",
  				&TestConfig::test_db_connector_config ));

      suiteOfTests->addTest(new CppUnit::TestCaller<TestConfig>("Test the md_connector_config function",
  				&TestConfig::test_md_connector_config ));

      suiteOfTests->addTest(new CppUnit::TestCaller<TestConfig>("Test the broker_connector_config function",
  				&TestConfig::test_broker_connector_config ));

  		return suiteOfTests;
  	}

  	void setUp() {
    }

  	void tearDown() {
    }

protected:
  void test_load_config(){
    bool returnValue;

    string correctConfig = "{\"MeasureData\" : {}, \"DataBaseConnector\" : {}, \"SLAConnectionHandler\" : {}}";
    string configWithoutMeasureData = "{\"DataBaseConnector\" : {}, \"SLAConnectionHandler\" : {}}";
    string configWithoutDataBaseConnector = "{\"MeasureData\" : {}, \"SLAConnectionHandler\" : {}}";
    string configWithoutSLAConnectionHandler = "{\"MeasureData\" : {}, \"DataBaseConnector\" : {}}";

    returnValue = testConfig->load_config(correctConfig);
    CPPUNIT_ASSERT(returnValue);

    returnValue = testConfig->load_config(configWithoutMeasureData);
    CPPUNIT_ASSERT(!returnValue);

    returnValue = testConfig->load_config(configWithoutDataBaseConnector);
    CPPUNIT_ASSERT(!returnValue);

    returnValue = testConfig->load_config(configWithoutSLAConnectionHandler);
    CPPUNIT_ASSERT(!returnValue);

  }

  void test_db_connector_config(){
    string dbConfig = "{\"MeasureData\" : {}, \"SLAConnectionHandler\" : {}, \"DataBaseConnector\":{\"PORT_NO\": 3306, \"DATABASE\": \"testdb\", \"HOSTNAME\": \"localhost\", \"USERNAME\": \"root\", \"PASSWORD\": \"root\", \"TABLES\": {\"Applications\": \"applications.txt\", \"Options\": \"options.txt\", \"Measurments\": \"measurments.txt\"}}}";

    testConfig->load_config(dbConfig);
    string HOSTNAME = "localhost";
    string DATABASE = "testdb";
    string USERNAME = "root";
    string PASSWORD = "root";
    int PORT_NO = 3306;

    CPPUNIT_ASSERT_EQUAL(testConfig->get_db_config().HOSTNAME, HOSTNAME);
    CPPUNIT_ASSERT_EQUAL(testConfig->get_db_config().DATABASE, DATABASE);
    CPPUNIT_ASSERT_EQUAL(testConfig->get_db_config().USERNAME, USERNAME);
    CPPUNIT_ASSERT_EQUAL(testConfig->get_db_config().PASSWORD, PASSWORD);
    CPPUNIT_ASSERT_EQUAL(testConfig->get_db_config().PORT_NO, PORT_NO);
  }

  void test_md_connector_config(){
    string mdConfig = "{\"MeasureData\" :  {\"MINUTES\": 42, \"SECONDS\": 44, \"HOURS\": 13, \"MAX_SIZE\": 42, \"MAX_WORKERS\": 2}, \"DataBaseConnector\" : {}, \"SLAConnectionHandler\" : {}}";
    testConfig->load_config(mdConfig);

    int MINUTES = 42;
    int SECONDS = 44;
    int HOURS = 13;
    int MAX_SIZE = 42;
    int MAX_WORKERS = 2;

    CPPUNIT_ASSERT_EQUAL(testConfig->get_md_config().MINUTES, MINUTES);
    CPPUNIT_ASSERT_EQUAL(testConfig->get_md_config().SECONDS, SECONDS);
    CPPUNIT_ASSERT_EQUAL(testConfig->get_md_config().HOURS, HOURS);
    CPPUNIT_ASSERT_EQUAL(testConfig->get_md_config().MAX_SIZE, MAX_SIZE);
    CPPUNIT_ASSERT_EQUAL(testConfig->get_md_config().MAX_WORKERS, MAX_WORKERS);
  }

  void test_broker_connector_config(){
    string brokerConfig = "{\"MeasureData\" : {}, \"DataBaseConnector\" : {}, \"SLAConnectionHandler\" : {\"PORT\": 5672, \"HOSTNAME\": \"10.0.2.15\", \"USERNAME\": \"guest\", \"PASSWORD\": \"guest\"}}";

    testConfig->load_config(brokerConfig);
    string HOSTNAME = "10.0.2.15";
    string USERNAME = "guest";
    string PASSWORD = "guest";
    int PORT = 5672;

    CPPUNIT_ASSERT_EQUAL(testConfig->get_broker_parameters().HOSTNAME, HOSTNAME);
    CPPUNIT_ASSERT_EQUAL(testConfig->get_broker_parameters().USERNAME, USERNAME);
    CPPUNIT_ASSERT_EQUAL(testConfig->get_broker_parameters().PASSWORD, PASSWORD);
    CPPUNIT_ASSERT_EQUAL(testConfig->get_broker_parameters().PORT, PORT);
  }

};
